## Description: the main python file to run.

# Import tool packages
from easydict import EasyDict as edict
from datetime import datetime
import os
import numpy as np
import json


# Import tool function
import utils
import brain_data

# Import model training phases
from train_phase1_model import train_phase1_model
from train_phase2_model import train_phase2_model
from train_phase3_model import train_phase3_model

def load_all_data(subject_id_list, label_list, data_dir):

    # get the list of sub csv for data augmentation
    sub_file_list = ['sub_{}.csv'.format(i) for i in subject_id_list]
    print('{} subjects'.format(len(sub_file_list)))
    print(sub_file_list)

    all_sub_data_list = []

    for sub_file in sub_file_list:

        sub_feature, sub_label = brain_data.read_subject_csv(os.path.join(data_dir, sub_file), label_list = label_list)

        sub_onehot_label = utils.convert_numpyarray_to_onehot(sub_label, class_number=len(label_list)).astype(np.float32)

        sub_data_dict = dict()
        sub_data_dict['sub_feature'] = sub_feature
        sub_data_dict['sub_onehot_label'] = sub_onehot_label

        all_sub_data_list.append(sub_data_dict)

    return all_sub_data_list

def run_one_parameter_set(hyper_params_dict, all_sub_data_list):
    # Seed
    seed = 0

    classification_type = hyper_params_dict['classification_type']
    phase_select = hyper_params_dict['phase_select']
    experiment_short_name = hyper_params_dict['experiment_short_name']

    # Shared arguments
    shared_params = edict()

    shared_params.result_save_rootdir = hyper_params_dict['result_save_rootdir']
    shared_params.train_select = hyper_params_dict['train_select']
    # shared_params.test_select = hyper_params_dict['test_select']

    # Shared parameters for CNN
    shared_params.window_size = hyper_params_dict['window_size']
    shared_params.window_stride = hyper_params_dict['window_stride']
    shared_params.conv1d_hidden_size = hyper_params_dict['conv1d_hidden_size']
    shared_params.linear_hidden_size = hyper_params_dict['linear_hidden_size']

    shared_params.label_list = hyper_params_dict['label_list']
    shared_params.num_classes = hyper_params_dict['num_classes']
    shared_params.feature_size = hyper_params_dict['feature_size']

    # Phase 1 args
    phase1_params = edict()

    phase1_params.restore_file = 'None'
    phase1_params.train_batch_size = hyper_params_dict['phase1_train_batch_size']
    phase1_params.lr = hyper_params_dict['phase1_lr']
    phase1_params.n_epoch = hyper_params_dict['phase1_n_epoch']
    phase1_params.alpha = hyper_params_dict['phase1_alpha']
    phase1_params.expand = hyper_params_dict['phase1_expand']

    # Phase 2 args
    phase2_params = edict()

    phase2_params.restore_file = 'phase1_model.statedict'
    phase2_params.train_batch_size = hyper_params_dict['phase2_train_batch_size']
    phase2_params.val_batch_size = hyper_params_dict['phase2_val_batch_size']
    phase2_params.lr = hyper_params_dict['phase2_lr']
    phase2_params.n_epoch = hyper_params_dict['phase2_n_epoch']

    # Phase 3 args
    phase3_params = edict()

    phase3_params.restore_file = 'phase2_best_model.statedict'
    phase3_params.cv_train_batch_size = hyper_params_dict['phase3_cv_train_batch_size']
    phase3_params.cv_val_batch_size = hyper_params_dict['phase3_cv_val_batch_size']
    phase3_params.test_batch_size = hyper_params_dict['phase3_test_batch_size']
    phase3_params.lr = hyper_params_dict['phase3_lr']
    phase3_params.n_epoch = hyper_params_dict['phase3_n_epoch']


    for cur_subject_index in range(len(hyper_params_dict['subject_id_list'])):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("\n\n")
        print("------------------- Class {}, Subject {}, Current Time {} -------------------"\
                .format(classification_type, hyper_params_dict['subject_id_list'][cur_subject_index], current_time))
        # print(experiment_params_str)
        print(hyper_params_dict['experiment_short_name'])
        print('train on ', hyper_params_dict['train_select'])
        # print('test on ', hyper_params_dict['test_select'])
        print('\n\n')

        # Initialize shared params of the current subject
        shared_params.SubjectId_of_interest = hyper_params_dict['subject_id_list'][cur_subject_index]
        shared_params.cur_subject_index = cur_subject_index

        utils.seed_everything(seed)

        if phase_select == 'allphases':
            # Run Phase 1
            print('\n' + 'Start MixUp pretraining'.center(100, '#') )
            train_phase1_model(shared_params, phase1_params, experiment_short_name, all_sub_data_list)
            print('Done MixUp pretraining'.center(100, '#') + '\n')
            # Run Phase 2
            print('\n' + 'Start group pretraining'.center(100, '#'))
            train_phase2_model(shared_params, phase2_params, experiment_short_name, all_sub_data_list)
            print('Done group pretraining'.center(100, '#') + '\n')
            # Run Phase 3
            print('\n' + 'Start personal training'.center(100, '#'))
            train_phase3_model(shared_params, phase3_params, experiment_short_name, all_sub_data_list)
            print('Done personal training'.center(100, '#') + '\n')

        elif phase_select == 'last2phases':
            phase2_params.restore_file = 'None'

            # Run Phase 2
            print('\n' + 'Start group pretraining'.center(100, '#'))
            train_phase2_model(shared_params, phase2_params, experiment_short_name, all_sub_data_list)
            print('Done group pretraining'.center(100, '#') + '\n')
            # Run Phase 3
            print('\n' + 'Start personal training'.center(100, '#'))
            train_phase3_model(shared_params, phase3_params, experiment_short_name, all_sub_data_list)
            print('Done personal training'.center(100, '#') + '\n')

        elif phase_select == 'baseline':
            phase3_params.restore_file = 'None'

            print('Start personal training'.center(100, '#'))
            train_phase3_model(shared_params, phase3_params, experiment_short_name, all_sub_data_list)
            print('Done personal training'.center(100, '#'))



def generate_hypermarameter_settings(hyper_param_searching_fields, hyper_params_fixed_dict):
    # Initialize the list to store all hyper params settings
    hyper_param_settings = []

    # Initialize the first hyper params setting
    hyper_params_dict = hyper_params_fixed_dict.copy()

    exp_count = 0

    # Classification search
    for classification_type_index in range(len(hyper_param_searching_fields['classification_type_list'])):
        classification_type = hyper_param_searching_fields['classification_type_list'][classification_type_index]
        label_list = hyper_param_searching_fields['label_list_list'][classification_type_index]
        hyper_params_dict['classification_type'] = classification_type
        hyper_params_dict['label_list'] = label_list
        hyper_params_dict['num_classes'] = len(label_list)
        # CNN search
        for window_size in hyper_param_searching_fields['window_size_list']:
            hyper_params_dict['window_size'] = window_size
            for window_stride in hyper_param_searching_fields['window_stride_list']:
                hyper_params_dict['window_stride'] = window_stride
                for conv1d_hidden_size in hyper_param_searching_fields['conv1d_hidden_size_list']:
                    hyper_params_dict['conv1d_hidden_size'] = conv1d_hidden_size
                    for linear_hidden_size in hyper_param_searching_fields['linear_hidden_size_list']:
                        hyper_params_dict['linear_hidden_size'] = linear_hidden_size

                        # Phase 1 search
                        for phase1_train_batch_size in hyper_param_searching_fields['phase1_train_batch_size_list']:
                            hyper_params_dict['phase1_train_batch_size'] = phase1_train_batch_size
                            for phase1_lr in hyper_param_searching_fields['phase1_lr_list']:
                                hyper_params_dict['phase1_lr'] = phase1_lr
                                for phase1_n_epoch in hyper_param_searching_fields['phase1_n_epoch_list']:
                                    hyper_params_dict['phase1_n_epoch'] = phase1_n_epoch
                                    for phase1_alpha in hyper_param_searching_fields['phase1_alpha_list']:
                                        hyper_params_dict['phase1_alpha'] = phase1_alpha
                                        for phase1_expand in hyper_param_searching_fields['phase1_expand_list']:
                                            hyper_params_dict['phase1_expand'] = phase1_expand

                                            # Phase 2 search
                                            for phase2_train_batch_size in hyper_param_searching_fields['phase2_train_batch_size_list']:
                                                hyper_params_dict['phase2_train_batch_size'] = phase2_train_batch_size
                                                for phase2_val_batch_size in hyper_param_searching_fields['phase2_val_batch_size_list']:
                                                    hyper_params_dict['phase2_val_batch_size'] = phase2_val_batch_size
                                                    for phase2_lr in hyper_param_searching_fields['phase2_lr_list']:
                                                        hyper_params_dict['phase2_lr'] = phase2_lr
                                                        for phase2_n_epoch in hyper_param_searching_fields['phase2_n_epoch_list']:
                                                            hyper_params_dict['phase2_n_epoch'] = phase2_n_epoch

                                                            # Phase 3 search
                                                            for phase3_cv_train_batch_size in hyper_param_searching_fields['phase3_cv_train_batch_size_list']:
                                                                hyper_params_dict['phase3_cv_train_batch_size'] = phase3_cv_train_batch_size
                                                                for phase3_cv_val_batch_size in hyper_param_searching_fields['phase3_cv_val_batch_size_list']:
                                                                    hyper_params_dict['phase3_cv_val_batch_size'] = phase3_cv_val_batch_size
                                                                    for phase3_test_batch_size in hyper_param_searching_fields['phase3_test_batch_size_list']:
                                                                        hyper_params_dict['phase3_test_batch_size'] = phase3_test_batch_size
                                                                        for phase3_lr in hyper_param_searching_fields['phase3_lr_list']:
                                                                            hyper_params_dict['phase3_lr'] = phase3_lr
                                                                            for phase3_n_epoch in hyper_param_searching_fields['phase3_n_epoch_list']:
                                                                                hyper_params_dict['phase3_n_epoch'] = phase3_n_epoch

                                                                                # Make short name
                                                                                if hyper_params_fixed_dict['phase_select'] == 'baseline':
                                                                                    hyper_params_dict['experiment_short_name'] = 'exp_' + str(exp_count) + '_baseline'
                                                                                    
                                                                                elif hyper_params_fixed_dict['phase_select'] == 'last2phases':
                                                                                    hyper_params_dict['experiment_short_name'] = 'exp_' + str(exp_count) + '_last2phases'

                                                                                elif hyper_params_fixed_dict['phase_select'] == 'allphases':
                                                                                    hyper_params_dict['experiment_short_name'] = 'exp_' + str(exp_count)
                                                                                
                                                                                # Store the current hyper params setting
                                                                                hyper_param_settings.append(hyper_params_dict)

                                                                                # Initialize the next hyper params setting
                                                                                hyper_params_dict = hyper_params_dict.copy()
                                                                                exp_count = exp_count + 1

    return hyper_param_settings

def filter_hyperparameter_settings(hyper_param_settings, param_name, param_value):
    filtered_setting_list = []
    for hyper_param_setting in hyper_param_settings:
        if hyper_param_setting[param_name] == param_value:
            filtered_setting_list.append(hyper_param_setting)
    return filtered_setting_list

if __name__ == "__main__":
    ######################### HyperParameters to set #########################
    # load qualified subject list
    subject_id_list = ['1', '3', '4', '5', '7',\
                        '8', '9', '10', '11', '12',\
                        '13', '14', '15', '16', '17',\
                        '18', '19', '20', '21', '22',\
                        '23', '24', '25', '26', '27', '28',\
                        '29']
    data_dir = '/home/leon/Documents/bci_research/code/data_augmentation/filtered_slide_window_data/task'

    phase_select = 'allphases'
    # phase_select = 'baseline'
    # phase_select = 'last2phases'


    # Totally we collect data of 16 tasks for each subject;
    # In phase3, we split 16 tasks into two parts: first 8 for train and last 8 for test;
    # In the training session of phase3, we choose to use data of full 8 tasks (100% of the training data) or half of them (50% of the training data) to evaluate if our algorithm can decrease individual calibration effort
    train_select = 'all_8_tasks'
    # train_select = 'first_4_tasks'
    # train_select = 'second_4_tasks'
    

    # make it multithreads working on the cluster
    thread_number = 9
    
    hyper_param_searching_fields = dict()

    # classification_type_list = ['binary_0_2', '4_class_0_1_2_3']
    # label_list_list = [[0,2],[0,1,2,3]]

    hyper_param_searching_fields['classification_type_list'] = ['binary_0_2']
    hyper_param_searching_fields['label_list_list'] = [[0,2]]

    # hyperparameters grid search for CNN
    hyper_param_searching_fields['window_size_list'] = [2, 4, 6]                # 3 values
    hyper_param_searching_fields['window_stride_list'] = [1, 2, 3]              # 3 values
    hyper_param_searching_fields['conv1d_hidden_size_list'] = [10, 20, 40]      # 3 values
    hyper_param_searching_fields['linear_hidden_size_list'] = [10, 20, 40]      # 3 values

    # hyperparameters grid search for Phase 1
    hyper_param_searching_fields['phase1_train_batch_size_list'] = [1000]
    hyper_param_searching_fields['phase1_lr_list'] = [0.01]
    hyper_param_searching_fields['phase1_n_epoch_list'] = [10]
    hyper_param_searching_fields['phase1_alpha_list'] = [0.3, 0.75, 0.9]        # 3 values
    hyper_param_searching_fields['phase1_expand_list'] = [2, 4, 8]              # 3 values

    # hyperparameters grid search for Phase 2
    hyper_param_searching_fields['phase2_train_batch_size_list'] = [1000]
    hyper_param_searching_fields['phase2_val_batch_size_list'] = [1000]
    hyper_param_searching_fields['phase2_lr_list'] = [0.01]
    hyper_param_searching_fields['phase2_n_epoch_list'] = [10]

    # hyperparameters grid search for Phase 3
    hyper_param_searching_fields['phase3_cv_train_batch_size_list'] = [890]
    hyper_param_searching_fields['phase3_cv_val_batch_size_list'] = [220]
    hyper_param_searching_fields['phase3_test_batch_size_list'] = [1000]
    hyper_param_searching_fields['phase3_lr_list'] = [0.003, 0.01, 0.03]        # 3 values
    hyper_param_searching_fields['phase3_n_epoch_list'] = [30]              # 2 values


    ####################### Fixed Hyperparameters #######################

    # Fixed hyperparameter
    hyper_params_fixed_dict = dict()
    hyper_params_fixed_dict['feature_size'] = 8
    hyper_params_fixed_dict['subject_id_list'] = subject_id_list
    hyper_params_fixed_dict['phase_select'] = phase_select
    hyper_params_fixed_dict['result_save_rootdir'] = result_save_rootdir
    # hyper_params_fixed_dict['test_select'] = test_select
    hyper_params_fixed_dict['train_select'] = train_select

    ####################### Auto Parameter Construction #######################
    hyper_param_settings = generate_hypermarameter_settings(hyper_param_searching_fields, hyper_params_fixed_dict)
    print("hyper param settings generated = {}".format(len(hyper_param_settings)))
    output_file_name = result_save_rootdir+'/'+'experiment_info.json'

    ############################## Filter out settings ##############################
    settings_ws2 = filter_hyperparameter_settings(hyper_param_settings, 'window_size', 2)
    settings_ws2_ws1 = filter_hyperparameter_settings(settings_ws2, 'window_stride', 1)
    settings_ws2_ws2 = filter_hyperparameter_settings(settings_ws2, 'window_stride', 2)
    settings_ws2_ws3 = filter_hyperparameter_settings(settings_ws2, 'window_stride', 3)
    
    settings_ws4 = filter_hyperparameter_settings(hyper_param_settings, 'window_size', 4)
    settings_ws4_ws1 = filter_hyperparameter_settings(settings_ws4, 'window_stride', 1)
    settings_ws4_ws2 = filter_hyperparameter_settings(settings_ws4, 'window_stride', 2)
    settings_ws4_ws3 = filter_hyperparameter_settings(settings_ws4, 'window_stride', 3)
    
    settings_ws6 = filter_hyperparameter_settings(hyper_param_settings, 'window_size', 6)
    settings_ws6_ws1 = filter_hyperparameter_settings(settings_ws6, 'window_stride', 1)
    settings_ws6_ws2 = filter_hyperparameter_settings(settings_ws6, 'window_stride', 2)
    settings_ws6_ws3 = filter_hyperparameter_settings(settings_ws6, 'window_stride', 3)

    if thread_number == 1:
        hyper_param_settings = settings_ws2_ws1
        output_file_name = result_save_rootdir+'/'+'experiment_info_0_242'
    elif thread_number == 2:
        hyper_param_settings = settings_ws2_ws2
        output_file_name = result_save_rootdir+'/'+'experiment_info_243_485'
    elif thread_number == 3:
        hyper_param_settings = settings_ws2_ws3
        output_file_name = result_save_rootdir+'/'+'experiment_info_486_728'
    elif thread_number == 4:
        hyper_param_settings = settings_ws4_ws1
        output_file_name = result_save_rootdir+'/'+'experiment_info_729_971'
    elif thread_number == 5:
        hyper_param_settings = settings_ws4_ws2
        output_file_name = result_save_rootdir+'/'+'experiment_info_972_1214'
    elif thread_number == 6:
        hyper_param_settings = settings_ws4_ws3
        output_file_name = result_save_rootdir+'/'+'experiment_info_1215_1457'
    elif thread_number == 7:
        hyper_param_settings = settings_ws6_ws1
        output_file_name = result_save_rootdir+'/'+'experiment_info_1458_1700'
    elif thread_number == 8:
        hyper_param_settings = settings_ws6_ws2
        output_file_name = result_save_rootdir+'/'+'experiment_info_1701_1943'
    elif thread_number == 9:
        hyper_param_settings = settings_ws6_ws3
        output_file_name = result_save_rootdir+'/'+'experiment_info_1944_2186'
    
    if phase_select == 'allphases':
        output_file_name = output_file_name + '.json'
    elif phase_select == 'baseline':
        output_file_name = output_file_name + '_baseline.json'
    elif phase_select == 'last2phases':
        output_file_name = output_file_name + '_last2phases.json'



    # Print out the first and last of selected settings
    print(hyper_param_settings[0]['experiment_short_name'], hyper_param_settings[-1]['experiment_short_name'])


    ############################## Load All Data ##############################
    # Load all subjects' data for all classification types
    sub_data_by_class = dict()
    classification_type = hyper_param_searching_fields['classification_type_list'][0]
    label_list = hyper_param_searching_fields['label_list_list'][0]
    all_sub_data_list = load_all_data(subject_id_list, label_list, data_dir)
    sub_data_by_class[classification_type] = all_sub_data_list

    ########################## Auto Parameter Search ##########################

    if os.path.exists(output_file_name):
        with open(output_file_name) as f:
            experiment_info_dict = json.load(f)
    else:
        experiment_info_dict = dict()

    # Run the experiment for each hyperparameter setting
    for hyper_param_setting in hyper_param_settings:
        # Skip the settings that are already finished
        if hyper_param_setting['experiment_short_name'] in experiment_info_dict:
            continue

        # Load the data for this classification type
        all_sub_data_list = sub_data_by_class[classification_type]

        # Run on this parameter setting
        run_one_parameter_set(hyper_param_setting, all_sub_data_list)
        
        # Store info
        experiment_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        experiment_short_name = hyper_param_setting['experiment_short_name']
        experiment_info_dict[experiment_short_name] = (experiment_time,hyper_param_setting)
        with open(output_file_name, 'w') as outfile:
            json.dump(experiment_info_dict, outfile)