## Description: work for allphases
# allphases: train on synthetic data generated from group subjects data and save the model for phase 2.

import os
import numpy as np
import torch
from tqdm import trange
import time

import models
import utils
import brain_data


def train_phase1_model(shared_params, phase1_params, experiment_name, all_sub_data_list):

    time_parse_params_start = time.time()

    # parse shared_params:
    result_save_rootdir = shared_params.result_save_rootdir
    SubjectId_of_interest = shared_params.SubjectId_of_interest
    cur_subject_index = shared_params.cur_subject_index

    # phase1_params
    restore_file = phase1_params.restore_file
    train_batch_size = phase1_params.train_batch_size 
    lr = phase1_params.lr 
    n_epoch = phase1_params.n_epoch
    alpha = phase1_params.alpha
    expand = phase1_params.expand
    
    # derived arg
    result_save_subjectdir = os.path.join(result_save_rootdir, SubjectId_of_interest, experiment_name)
    result_save_subject_checkpointdir = os.path.join(result_save_subjectdir, 'checkpoint')
    result_save_subject_trainingcurvedir = os.path.join(result_save_subjectdir, 'trainingcurve')

    utils.makedir_if_not_exist(result_save_subjectdir)
    utils.makedir_if_not_exist(result_save_subject_checkpointdir)
    utils.makedir_if_not_exist(result_save_subject_trainingcurvedir)

    # torch setting
    cuda = torch.cuda.is_available()
    if cuda:
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')


    #  TODO: remove the timer
    time_load_data_start = time.time()
    print('Phase 1 parse params duration: {}seconds'.format(time_load_data_start - time_parse_params_start))

    # get the features and labels for these subjects
    prior_sub_feature_list = []
    prior_sub_onehot_label_list = []

    for sub_index in range(len(all_sub_data_list)):
        # Skip the data of the current subject
        if cur_subject_index == sub_index:
            continue

        sub_feature = all_sub_data_list[sub_index]['sub_feature']
        sub_onehot_label = all_sub_data_list[sub_index]['sub_onehot_label']

        train_row_number = sub_onehot_label.shape[0]
        
        prior_sub_feature_list.append(sub_feature[:train_row_number])
        prior_sub_onehot_label_list.append(sub_onehot_label[:train_row_number])


    # The result is 4D (number of subjects, number of chunks of each subject, row number of each chunk, column number of each chunk)
    
    prior_sub_feature_array = np.array(prior_sub_feature_list)
    prior_sub_onehot_label_array = np.array(prior_sub_onehot_label_list)

    print('Phase 1 {} subjects'.format(prior_sub_feature_array.shape))  

    time_load_data_end = time.time()
    print('Phase 1 load data duration: {}seconds'.format(time_load_data_end - time_load_data_start))

    # create synthetic data via MixUp
    mixup_sub_feature_array, mixup_sub_onehot_label_array = utils.MixUp_expansion(prior_sub_feature_array, prior_sub_onehot_label_array, alpha=alpha, expand=expand)

    time_mixup_end = time.time()
    print('Phase 1 MixUp duration: {}seconds'.format(time_mixup_end - time_load_data_end))

    # Concatenate all subjects
    # The result array is 3D (total chunk number of all subjects, rows of each chunk, columns of each chunk)
    mixup_sub_feature_array = np.concatenate(mixup_sub_feature_array, axis=0).astype(np.float32)
    mixup_sub_onehot_label_array = np.concatenate(mixup_sub_onehot_label_array, axis=0).astype(np.float32)

    # Convert to dataset object
    mixup_train_set = brain_data.brain_dataset(mixup_sub_feature_array, mixup_sub_onehot_label_array)

    # Convert to dataloader
    mixup_train_loader = torch.utils.data.DataLoader(mixup_train_set, batch_size=train_batch_size, shuffle=True)

    #  TODO: remove the timer
    time_data_loader_end = time.time()
    print('Phase 1 create data loader duration: {}seconds'.format(time_data_loader_end - time_mixup_end))

    # Create model

    num_classes = shared_params.num_classes
    feature_size = shared_params.feature_size

    # Searchable hyperparameters
    window_size = shared_params.window_size
    window_stride = shared_params.window_stride
    conv1d_hidden_size = shared_params.conv1d_hidden_size
    linear_hidden_size = shared_params.linear_hidden_size

    # Instanciate a model
    model = models.SimpleCNN(feature_size, conv1d_hidden_size, window_size, window_stride, linear_hidden_size, num_classes).to(device)

    # Reload weights from restore_file is specified
    if restore_file != 'None':
        restore_path = os.path.join(os.path.join(result_save_subject_checkpointdir, restore_file))
        print('loading checkpoint: {}'.format(restore_path))
        model.load_state_dict(torch.load(restore_path, map_location=device))


    # Create criterion and optimizer
    criterion = utils.soft_cross_entropy
    optimizer = torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9)


    # Training loop
    epoch_train_loss = []
    for epoch in trange(n_epoch, desc = 'Training Phase1'):
        average_loss_this_epoch = utils.train_one_epoch(model, optimizer, criterion, mixup_train_loader, device, 'SimpleCNN')
        epoch_train_loss.append(average_loss_this_epoch)

    time_train_end = time.time()
    print('Phase 1 train duration: {}seconds'.format(time_train_end - time_data_loader_end))

    # save training curve for phase1
    # utils.save_training_curves('phase1_training_curve.png', result_save_subject_trainingcurvedir, epoch_train_loss)
    utils.save_training_curves_json('phase1_training_curve.json', result_save_subject_trainingcurvedir, epoch_train_loss)


    # save the model at last epoch
    torch.save(model.state_dict(), os.path.join(result_save_subject_checkpointdir, 'phase1_model.statedict'))


    time_save_model_end = time.time()
    print('Phase 1 save model duration: {}seconds'.format(time_save_model_end - time_train_end))