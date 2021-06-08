## Description: work for allphases, last2phases and baseline.
# 1. allphases, last2phases: load the model generated from phase 2, train on the individual subject's training data, and test on his/her test data.
# 2. baseline: train on the individual subject's training data, and test on his/her test data.
import os
import numpy as np
import torch
from tqdm import trange
import time

import models
import utils
import brain_data

from sklearn.model_selection import KFold

#for personal model, save the test prediction of each cv fold
def train_phase3_model(shared_params, phase3_params, experiment_name, all_sub_data_list):
    time_parse_params_start = time.time()

    # parse shared_params:
    result_save_rootdir = shared_params.result_save_rootdir
    train_select = shared_params.train_select
    SubjectId_of_interest = shared_params.SubjectId_of_interest
    cur_subject_index = shared_params.cur_subject_index
    label_list = shared_params.label_list

    # phase3_params
    restore_file = phase3_params.restore_file
    cv_train_batch_size = phase3_params.cv_train_batch_size 
    cv_val_batch_size = phase3_params.cv_val_batch_size
    test_batch_size = phase3_params.test_batch_size 
    lr = phase3_params.lr 
    n_epoch = phase3_params.n_epoch 

    # derived arg
    result_save_subjectdir = os.path.join(result_save_rootdir, SubjectId_of_interest, experiment_name)
    result_save_subject_checkpointdir = os.path.join(result_save_subjectdir, 'checkpoint')
    result_save_subject_predictionsdir = os.path.join(result_save_subjectdir, 'predictions')
    result_save_subject_resultanalysisdir = os.path.join(result_save_subjectdir, 'result_analysis')
    result_save_subject_trainingcurvedir = os.path.join(result_save_subjectdir, 'trainingcurve')

    utils.makedir_if_not_exist(result_save_subjectdir)
    utils.makedir_if_not_exist(result_save_subject_checkpointdir)
    utils.makedir_if_not_exist(result_save_subject_predictionsdir)
    utils.makedir_if_not_exist(result_save_subject_resultanalysisdir)
    utils.makedir_if_not_exist(result_save_subject_trainingcurvedir)
  
    #torch setting
    cuda = torch.cuda.is_available()
    if cuda:
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')


    time_load_data_start = time.time()
    print('Phase 3 parse params duration: {}seconds'.format(time_load_data_start - time_parse_params_start))

    sub_feature_array = all_sub_data_list[cur_subject_index]['sub_feature']
    sub_onehot_label_array = all_sub_data_list[cur_subject_index]['sub_onehot_label']

    time_load_data_end = time.time()
    print('Phase 3 load data duration: {}seconds'.format(time_load_data_end - time_load_data_start))

    # Totally we collect data of 16 tasks for each subject;
    # We split 16 tasks into two parts: first 8 for train and last 8 for test;
    # In the training session, we choose to use data of full 8 tasks (100% of the training data) or half of them (50% of the training data) to evaluate if our algorithm can decrease individual calibration effort
    if train_select == 'all_8_tasks':
        start_train_row_number = 0
        end_train_row_number = int(sub_onehot_label_array.shape[0] * 0.5)
    elif train_select == 'first_4_tasks':
        start_train_row_number = 0
        end_train_row_number = int(sub_onehot_label_array.shape[0] * 0.25)
    elif train_select == 'second_4_tasks':
        start_train_row_number = int(sub_onehot_label_array.shape[0] * 0.25)
        end_train_row_number = int(sub_onehot_label_array.shape[0] * 0.5)

    # Use the last 8 tasks as test data for each subject
    start_test_row_number = int(sub_onehot_label_array.shape[0] * 0.5)
    end_test_row_number = sub_onehot_label_array.shape[0]

    sub_train_feature_array = sub_feature_array[start_train_row_number:end_train_row_number]
    sub_train_onehot_label_array = sub_onehot_label_array[start_train_row_number:end_train_row_number]

    sub_test_feature_array = sub_feature_array[start_test_row_number:end_test_row_number]
    sub_test_onehot_label_array = sub_onehot_label_array[start_test_row_number:end_test_row_number]
    
    # Convert subject's test data into dataset object
    sub_test_set = brain_data.brain_dataset(sub_test_feature_array, sub_test_onehot_label_array)
    
    # Convert subject's test dataset object into dataloader object
    sub_test_loader = torch.utils.data.DataLoader(sub_test_set, batch_size=test_batch_size, shuffle=False)

    time_data_loader_end = time.time()
    print('Phase 3 create data loader duration: {}seconds'.format(time_data_loader_end - time_load_data_end))

    #cross validation:
    phase3_save_dict = dict()
    
    kf = KFold(n_splits=5, shuffle=False, random_state=1)
    for idx, (train_index, val_index) in enumerate(kf.split(sub_train_feature_array)):
        # print('idx={}, train_index={}'.format(idx, train_index))
        # print('idx={}, val_index={}'.format(idx, val_index))

        val_index = val_index[3:-3]

        # dataset object
        sub_cv_train_set = brain_data.brain_dataset(sub_train_feature_array[train_index], sub_train_onehot_label_array[train_index])
        sub_cv_val_set = brain_data.brain_dataset(sub_train_feature_array[val_index], sub_train_onehot_label_array[val_index])

        # dataloader object
        sub_cv_train_loader = torch.utils.data.DataLoader(sub_cv_train_set, batch_size=cv_train_batch_size, shuffle=True) 
        sub_cv_val_loader = torch.utils.data.DataLoader(sub_cv_val_set, batch_size=cv_val_batch_size, shuffle=False)

        # Create model
    
        num_classes = shared_params.num_classes
        feature_size = shared_params.feature_size

        # searchable hyperparameters
        window_size = shared_params.window_size
        window_stride = shared_params.window_stride
        conv1d_hidden_size = shared_params.conv1d_hidden_size
        linear_hidden_size = shared_params.linear_hidden_size

        model = models.SimpleCNN(feature_size, conv1d_hidden_size, window_size, window_stride, linear_hidden_size, num_classes).to(device)

        # reload weights from restore_file is specified
        # "None" value for running phase3 (personal model) only
        if restore_file != 'None':
            restore_path = os.path.join(os.path.join(result_save_subject_checkpointdir, restore_file))
            print('loading checkpoint: {}'.format(restore_path))
            model.load_state_dict(torch.load(restore_path, map_location=device))

        # create criterion and optimizer
        criterion = utils.soft_cross_entropy
        optimizer = torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9)

        # training loop
        best_val_accuracy = 0.0
        
        epoch_train_loss = []
        epoch_validation_accuracy = []
        
        for epoch in trange(n_epoch, desc='Training Phase3, CV fold{}'.format(idx)):
            average_loss_this_epoch = utils.train_one_epoch(model, optimizer, criterion, sub_cv_train_loader, device, 'SimpleCNN')
            val_accuracy, _, _, _ = utils.eval_model(model, sub_cv_val_loader, device, 'SimpleCNN')
            
            epoch_train_loss.append(average_loss_this_epoch)
            epoch_validation_accuracy.append(val_accuracy)
            
            #update is_best flag
            is_best = val_accuracy >= best_val_accuracy

            if is_best:
                best_val_accuracy = val_accuracy

                torch.save(model.state_dict(), os.path.join(result_save_subject_checkpointdir, 'phase3_fold{}_best_model.statedict'.format(idx)))

                test_accuracy, test_class_predictions, test_class_labels, test_logits = utils.eval_model(model, sub_test_loader, device, model_class = 'SimpleCNN')
                print('test accuracy for this fold is {}'.format(test_accuracy))
                
                phase3_save_dict['fold{}_bestepoch_test_accuracy'.format(idx)] = test_accuracy
                phase3_save_dict['fold{}_bestepoch_val_accuracy'.format(idx)] = val_accuracy

                phase3_save_dict['fold{}_bestepoch_test_logits'.format(idx)] = test_logits.copy()
                phase3_save_dict['fold{}_bestepoch_test_class_labels'.format(idx)] = test_class_labels.copy()
                
        
        #save training curve for each fold for phase3
        # utils.save_training_curves('phase3_fold{}_training_curve.png'.format(idx), result_save_subject_trainingcurvedir, epoch_train_loss, epoch_validation_accuracy)
        utils.save_training_curves_json('phase3_fold{}_training_curve.json'.format(idx), result_save_subject_trainingcurvedir, epoch_train_loss, epoch_validation_accuracy)
        
        #confusion matrix for this fold
        # utils.plot_confusion_matrix(test_class_predictions, test_class_labels, label_list, result_save_subject_resultanalysisdir, 'fold{}_test_confusion_matrix.png'.format(idx))
        utils.plot_confusion_matrix_json(test_class_predictions, test_class_labels, label_list, result_save_subject_resultanalysisdir, 'fold{}_test_confusion_matrix.json'.format(idx))
        
        #save the model at last epoch
        torch.save(model.state_dict(), os.path.join(result_save_subject_checkpointdir, 'phase3_fold{}_last_model.statedict'.format(idx)))

    time_train_end = time.time()
    print('Phase 3 train duration: {}seconds'.format(time_train_end - time_data_loader_end))

    #save phase3_save_dict
    utils.save_pickle(result_save_subject_predictionsdir, 'phase3_save_dict.pkl', phase3_save_dict)
        
        
    #perform result analysis
    #ensemble of the 5 folds for ensembled test predictions
    bagging_test_accuracy = utils.ensemble_and_extract_performance(model.state_dict(), result_save_subject_predictionsdir, result_save_subject_resultanalysisdir)
    print('Ensembled test accuracy for 5 folds is {}'.format(bagging_test_accuracy))

    time_save_model_end = time.time()
    print('Phase 3 save model duration: {}seconds'.format(time_save_model_end - time_train_end))