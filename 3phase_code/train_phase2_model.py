## Description: work for allphases and last2phases
# 1. allphases: load the model generated from phase 1, train on real group subjects' data and save it for phase 3.
# 2. last2phases: train on real group subjects' data and save the model for phase 3.

import os
import numpy as np
import torch
from tqdm import trange
import time

import models
import utils
import brain_data


def train_phase2_model(shared_params, phase2_params, experiment_name, all_sub_data_list):
    #  TODO: remove the timer
    time_parse_params_start = time.time()

    # for group model only need train and val set

    # parse shared_params:
    result_save_rootdir = shared_params.result_save_rootdir
    SubjectId_of_interest = shared_params.SubjectId_of_interest

    # phase2_params
    restore_file = phase2_params.restore_file
    train_batch_size = phase2_params.train_batch_size 
    val_batch_size = phase2_params.val_batch_size
    lr = phase2_params.lr 
    n_epoch = phase2_params.n_epoch 

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
    print('Phase 2 parse params duration: {}seconds'.format(time_load_data_start - time_parse_params_start))

    # get the features and labels for these subjects
    group_model_sub_train_feature_list = []
    group_model_sub_train_onehot_label_list = []
    group_model_sub_val_feature_list = []
    group_model_sub_val_onehot_label_list = []


    # Use the last 1/4 of the chunks for each subject as validation dataset
    for sub_index in range(len(all_sub_data_list)):
        sub_feature = all_sub_data_list[sub_index]['sub_feature']
        sub_onehot_label = all_sub_data_list[sub_index]['sub_onehot_label']

        # Use the last 1/4 of the chunks for each subject as validation dataset
        # TODO: Make Validation row number a parameter
        train_row_number = int(sub_onehot_label.shape[0] * 0.75)
        val_row_number = int(sub_onehot_label.shape[0] * 0.25)

        group_model_sub_train_feature_list.append(sub_feature[:train_row_number])
        group_model_sub_train_onehot_label_list.append(sub_onehot_label[:train_row_number])
    
        group_model_sub_val_feature_list.append(sub_feature[train_row_number:(train_row_number+val_row_number)])
        group_model_sub_val_onehot_label_list.append(sub_onehot_label[train_row_number:(train_row_number+val_row_number)])

    # The result is 4D (number of subjects, number of train(1668)/validation(556) chunks of each subject, row number of each chunk, column number of each chunk)

    group_model_sub_train_feature_array = np.array(group_model_sub_train_feature_list)
    group_model_sub_train_onehot_label_array = np.array(group_model_sub_train_onehot_label_list)
    group_model_sub_val_feature_array = np.array(group_model_sub_val_feature_list)
    group_model_sub_val_onehot_label_array = np.array(group_model_sub_val_onehot_label_list)

    print('Phase 2 {} subjects'.format(group_model_sub_train_feature_array.shape))

    #  TODO: remove the timer
    time_load_data_end = time.time()
    print('Phase 2 load data duration: {}seconds'.format(time_load_data_end - time_load_data_start))

    # Concatenate all subjects
    # The result array is 3D (total chunk number of all subjects, rows of each chunk, columns of each chunk)
    group_train_feature = np.concatenate(group_model_sub_train_feature_array, axis=0).astype(np.float32)
    group_train_onehot_label = np.concatenate(group_model_sub_train_onehot_label_array, axis=0).astype(np.float32)

    group_val_feature = np.concatenate(group_model_sub_val_feature_array, axis = 0).astype(np.float32)
    group_val_onehot_label = np.concatenate(group_model_sub_val_onehot_label_array, axis = 0).astype(np.float32)

    print('group_train_feature.shape: {}'.format(group_train_feature.shape))
    print('group_train_label.shape: {}'.format(group_train_onehot_label.shape))
    print('group_val_feature.shape: {}'.format(group_val_feature.shape))
    print('group_val_label.shape: {}'.format(group_val_onehot_label.shape))

    # Convert to dataset object
    group_train_set = brain_data.brain_dataset(group_train_feature, group_train_onehot_label)
    group_val_set = brain_data.brain_dataset(group_val_feature, group_val_onehot_label)


    # Convert to dataloader
    group_train_loader = torch.utils.data.DataLoader(group_train_set, batch_size = train_batch_size, shuffle=True)
    group_val_loader = torch.utils.data.DataLoader(group_val_set, batch_size = val_batch_size, shuffle=False)

    time_data_loader_end = time.time()
    print('Phase 2 create data loader duration: {}seconds'.format(time_data_loader_end - time_load_data_end))

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

    # reload weights from restore_file is specified
    if restore_file != 'None':
        restore_path = os.path.join(os.path.join(result_save_subject_checkpointdir, restore_file))
        print('loading checkpoint: {}'.format(restore_path))
        model.load_state_dict(torch.load(restore_path, map_location=device))

    time_load_model_end = time.time()
    print('Phase 2 load model duration: {}seconds'.format(time_load_model_end - time_data_loader_end))

    # create criterion and optimizer
    criterion = utils.soft_cross_entropy
    optimizer = torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9)

    # Training loop
    best_val_accuracy = 0.0

    epoch_train_loss = []
    epoch_validation_accuracy = []
    
    for epoch in trange(n_epoch, desc = 'Training Phase2'):
        average_loss_this_epoch = utils.train_one_epoch(model, optimizer, criterion, group_train_loader, device, 'SimpleCNN')
        epoch_train_loss.append(average_loss_this_epoch)

        val_accuracy, _, _, _ = utils.eval_model(model, group_val_loader, device, 'SimpleCNN')
        epoch_validation_accuracy.append(val_accuracy)
        
        #update is_best flag
        is_best = val_accuracy >= best_val_accuracy
        
        if is_best:
            best_val_accuracy = val_accuracy
            
            torch.save(model.state_dict(), os.path.join(result_save_subject_checkpointdir, 'phase2_best_model.statedict'))

    
    time_train_end = time.time()
    print('Phase 2 train duration: {}seconds'.format(time_train_end - time_load_model_end))

    # save training curve for phase2
    # utils.save_training_curves('phase2_training_curve.png', result_save_subject_trainingcurvedir, epoch_train_loss, epoch_validation_accuracy)
    utils.save_training_curves_json('phase2_training_curve.json', result_save_subject_trainingcurvedir, epoch_train_loss, epoch_validation_accuracy)
    
    #save the model at last epoch
    torch.save(model.state_dict(), os.path.join(result_save_subject_checkpointdir, 'phase2_last_model.statedict'))

    time_save_model_end = time.time()
    print('Phase 2 save model duration: {}seconds'.format(time_save_model_end - time_train_end))