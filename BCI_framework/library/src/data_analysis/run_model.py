from . import models
from . import logger as customized_logger
from .brain_data import personal_brain_data, read_data_single
from .utils import pickle_to_file, eval_model, eval_model_single_chunk, write_stats_csv, write_model_info

# from .utils import process_with_sliding_window, plot_test_performance_bar, plot_train_val_loss, plot_learning_rate_schedule, plot_test_performance_lineplot



# import models
# import logger as customized_logger
# from brain_data import personal_brain_data, read_data_single
# from utils import pickle_to_file, eval_model, eval_model_single_chunk, write_stats_csv, write_model_info


import torch
import torch.nn as nn
import torch.nn.functional as F

import pandas as pd
import numpy as np
import sys
import os
import time
import datetime
import pickle
import glob

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import KFold




def run(param_dict):
    program_start_time = time.time()


    train_dir = param_dict["train_dir"]
    train_files = param_dict["train_files"]
    load_mode = param_dict["load_mode"]
    col_index = param_dict["col_index"]
    feature_index = param_dict["feature_index"]

    #################### Initialize cuda device setting ####################
    cuda = torch.cuda.is_available()
    if cuda:
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    
    
    result_save_path = create_result_save_path(param_dict)

    #################### Initialize logger ####################
    logger_confusion_matrix = create_logger(result_save_path)

    log_general_info(logger_confusion_matrix, param_dict, device, result_save_path)
    

    #################### Load Train/Test Data ####################
    # Load Train Set
    total_train_instances, total_train_labels = load_train_data(train_dir, train_files, load_mode, col_index, feature_index)

    # Load Test Set
    # test set is not needed for cross validation
    '''
    test_instances, test_labels = load_train_data(test_dir, test_files, load_mode)
    test_set = personal_brain_data(test_instances, test_labels)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size = test_batch_size, shuffle = False)
    '''

    ########################### Cross Validation and Grid Search ########################
    best_LAMBDA = grid_search_cross_validation(result_save_path, param_dict, total_train_instances, total_train_labels, device) # test_loader

    print("------------------------------------------------------------------------\n\n")
    print("Best LAMBDA {}".format(best_LAMBDA))
    print("\n\n------------------------------------------------------------------------")

    ########################### Train Final Model Using Best Hyper Parameters ########################
    group_count = 1
    log_dict, people_best_models = train_model_using_best_hyper_params(result_save_path, param_dict, total_train_instances, total_train_labels, device, best_LAMBDA, group_count, logger_confusion_matrix) #test_loader test_files
    

    ########################### Save Log Info For Final Model ########################
    save_log_list(result_save_path, log_dict)


    log_total_time(logger_confusion_matrix, program_start_time)
    return people_best_models

def create_result_save_path(param_dict):
    initialized = param_dict["initialized"]
    model_class = param_dict["model_class"]

    load_group_model_path = param_dict["load_group_model_path"]

    train_batch_size = param_dict["train_batch_size"]
    learning_rate = param_dict["learning_rate"]
    

    result_save_dir = param_dict["result_save_dir"]

    #################### Initialize Path for Saving Model ####################
    if initialized:
        #use folder name to indicate where the model initialized from
        initialized_from = 'group_model_' + load_group_model_path.split('/')[-2]

        result_save_subdir = model_class + '/'+ 'from_'+ initialized_from + '/' + 'batch_'+ str(train_batch_size) + '_lr_' + str(learning_rate) + '_FixedLR/'
    
    else:
        result_save_subdir = model_class + '/' + 'from_scratch/' + 'batch_'+ str(train_batch_size) + '_lr_' + str(learning_rate) + '_FixedLR/'
    
    #create save dir if save dir not already exist
    result_save_path = os.path.join(result_save_dir, result_save_subdir)
    if not os.path.exists(result_save_path):
        print('Creating new save dir!!!!')
        os.makedirs(result_save_path)
    
    return result_save_path
    
def create_logger(result_save_path):
    #create a logger specifically for confusion matrix
    log_file_name_confusion_matrix = 'single_person_confusion_matrix'+ str(datetime.datetime.now()) +'.log'
    logger_confusion_matrix = customized_logger.logger(result_save_path, log_file_name_confusion_matrix)
    logger_confusion_matrix.log('############Logger constructed!###########\n')
    return logger_confusion_matrix

def log_general_info(logger_confusion_matrix, param_dict, device, result_save_path):
    n_epoch = param_dict["n_epoch"]
    train_batch_size = param_dict["train_batch_size"]
    val_batch_size = param_dict["val_batch_size"]
    eval_every_iteration = param_dict["eval_every_iteration"]
    learning_rate = param_dict["learning_rate"]
    input_size = param_dict["input_size"]
    num_classes = param_dict["num_classes"]

    train_dir = param_dict["train_dir"]

    initialized = param_dict["initialized"]
    load_group_model_path = param_dict["load_group_model_path"]

    gpu_index = param_dict["gpu_index"]

    logger_confusion_matrix.log('Experiment Setting: \n')
    logger_confusion_matrix.log('device is: {}'.format(device))
    logger_confusion_matrix.log('n_epoch:{}\t\t, train_batch_size:{}\t\t, val_batch_size:{}\t\t, eval_every_iteration:{}\t\t, learning_rate:{}\t\t, input_size:{}\t\t, num_classes:{}\t\t, result_save_path:{}\t\t, train_dir:{}\t\t\t\t, load_group_model_path:{}\t\t, initialized:{}\t\t, gpu_index:{}\t\t'.format(n_epoch, train_batch_size, val_batch_size, eval_every_iteration, learning_rate, input_size, num_classes, result_save_path, train_dir, load_group_model_path, initialized, gpu_index))
    
    logger_confusion_matrix.flush()

def grid_search_cross_validation(result_save_path, param_dict, total_train_instances, total_train_labels, device): # test_loader ()

    #################### Initialize Common Parameters ####################
    model_class = param_dict["model_class"]
    n_epoch = param_dict["n_epoch"]
    train_batch_size = param_dict["train_batch_size"]
    val_batch_size = param_dict["val_batch_size"]
    
    eval_every_iteration = param_dict["eval_every_iteration"]
    learning_rate = param_dict["learning_rate"]
    input_size = param_dict["input_size"]
    
    num_classes = param_dict["num_classes"]
    
    
    initialized = param_dict["initialized"]
    load_group_model_path = param_dict["load_group_model_path"]

    #################### Initialize Model Specific Parameters ####################
    if model_class == 'SimpleRNN':
        model_to_use = models.SimpleRNN
        
        hidden_size = param_dict["hidden_size"]
        num_layers = param_dict["num_layers"]
        num_directions = param_dict["num_directions"]
        
        hidden_size, num_layers, num_directions = map(int, [hidden_size, num_layers, num_directions])
        
    elif model_class == 'LSTM':
        model_to_use = models.BiRNN #BiRNN is not a good name, change later 

        hidden_size = param_dict["hidden_size"]
        num_layers = param_dict["num_layers"]
        num_directions = param_dict["num_directions"]
        
        hidden_size, num_layers, num_directions = map(int, [hidden_size, num_layers, num_directions])
        
    elif model_class == 'LogisticRegression':
        model_to_use = models.LogisticRegression
        
    elif model_class == 'CNN':
        print('Using CNN', flush = True)
        model_to_use = models.CNN
        
        conv1d_hidden_size = param_dict["conv1d_hidden_size"]
        window_size = param_dict["window_size"]
        window_stride = param_dict["window_stride"]
        linear_hidden_size = param_dict["linear_hidden_size"]


    temp_file_name = os.path.join(result_save_path,'cross_validation_grid_search.txt')


    ########################### Cross Validation and Grid Search Start ########################
    params_to_search = dict(
        L2_LAMBDA=np.logspace(-3, 3, 5).tolist(),
    #         beta=np.logspace(-3, 3, 7 + 12).tolist(),
        )
    
    kf = KFold(n_splits=3)
    
    cross_validation_writer = open(temp_file_name, 'w')
    validation_accuracy_for_different_LAMBDA = []

    ########################### Try all sets of hyper parameters ########################
    for L2_LAMBDA in params_to_search['L2_LAMBDA']:

        validation_accuracy_for_this_LAMBDA = []
        for train_index, val_index in kf.split(total_train_instances):
            #print("TRAIN:", train_index, "VAL:", val_index)
            #Train/Val/Test dataset object
            train_set = personal_brain_data(total_train_instances[train_index], total_train_labels[train_index])
            val_set = personal_brain_data(total_train_instances[val_index], total_train_labels[val_index])

            #Dataloader
            kf_train_loader = torch.utils.data.DataLoader(train_set, batch_size = train_batch_size, shuffle = True)
            kf_val_loader = torch.utils.data.DataLoader(val_set, batch_size = val_batch_size, shuffle = False)

            #Create model:
            if model_class == 'SimpleRNN' or model_class == 'LSTM':
                model = model_to_use(input_size, hidden_size, num_layers, num_classes, num_directions, device).to(device)

            if model_class == 'LogisticRegression':
                model = model_to_use(input_size, num_classes).to(device)

            if model_class == 'CNN':
                model = model_to_use(input_size, conv1d_hidden_size, window_size, window_stride , linear_hidden_size, num_classes).to(device)

            #Loss function and optimizer 
            criterion = nn.CrossEntropyLoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

            best_val_accuracy = 0
            global_step = 0

            for epoch in range(n_epoch):
                global_step += 1

                _, _, _, _, _ = train_model(model, optimizer, criterion, kf_train_loader, L2_LAMBDA, device, model_class, train_only_last_layer=False)

                if global_step % eval_every_iteration == 0:
                    validation_accuracy, _, _, _ = eval_model(model, kf_val_loader, device, model_class)

                    if validation_accuracy > best_val_accuracy:
                        best_val_accuracy = validation_accuracy

            print('best_val_accuracy for this fold: {}'.format(best_val_accuracy))
            validation_accuracy_for_this_LAMBDA.append(best_val_accuracy)

        average_validation_accuracy_for_this_LAMBDA = np.mean(np.array(validation_accuracy_for_this_LAMBDA))
        print('\naverage_val_accuracy for this LAMBDA: {}\n\n'.format(average_validation_accuracy_for_this_LAMBDA))
        cross_validation_writer.write('\naverage_val_accuracy for this LAMBDA: {}\n\n'.format(average_validation_accuracy_for_this_LAMBDA))

        validation_accuracy_for_different_LAMBDA.append(average_validation_accuracy_for_this_LAMBDA)
    ########################### Find the best hyper parameter ########################
    best_LAMBDA_id = np.argmax(np.array(validation_accuracy_for_different_LAMBDA))
    best_LAMBDA = params_to_search['L2_LAMBDA'][best_LAMBDA_id]

    print('\n\nbest_LAMBDA is {}'.format(best_LAMBDA))
    cross_validation_writer.write('\n\nbest_LAMBDA is {}'.format(best_LAMBDA))
    ########################### Cross Validation and Grid Search End ########################
    return best_LAMBDA

def train_model_using_best_hyper_params(result_save_path, param_dict, total_train_instances, total_train_labels, device, best_LAMBDA, group_count, logger_confusion_matrix):#test_loader test_files
    #################### Initialize Common Parameters ####################
    model_class = param_dict["model_class"]
    n_epoch = param_dict["n_epoch"]
    train_batch_size = param_dict["train_batch_size"]
    val_batch_size = param_dict["val_batch_size"]
    
    eval_every_iteration = param_dict["eval_every_iteration"]
    learning_rate = param_dict["learning_rate"]
    input_size = param_dict["input_size"]
    
    num_classes = param_dict["num_classes"]


    initialized = param_dict["initialized"]
    load_group_model_path = param_dict["load_group_model_path"]

    #################### Initialize Model Specific Parameters ####################
    if model_class == 'SimpleRNN':
        model_to_use = models.SimpleRNN
        
        hidden_size = param_dict["hidden_size"]
        num_layers = param_dict["num_layers"]
        num_directions = param_dict["num_directions"]
        
        hidden_size, num_layers, num_directions = map(int, [hidden_size, num_layers, num_directions])
        
    elif model_class == 'LSTM':
        model_to_use = models.BiRNN #BiRNN is not a good name, change later 

        hidden_size = param_dict["hidden_size"]
        num_layers = param_dict["num_layers"]
        num_directions = param_dict["num_directions"]
        
        hidden_size, num_layers, num_directions = map(int, [hidden_size, num_layers, num_directions])
        
    elif model_class == 'LogisticRegression':
        model_to_use = models.LogisticRegression
        
    elif model_class == 'CNN':
        print('Using CNN', flush = True)
        model_to_use = models.CNN
        
        conv1d_hidden_size = param_dict["conv1d_hidden_size"]
        window_size = param_dict["window_size"]
        window_stride = param_dict["window_stride"]
        linear_hidden_size = param_dict["linear_hidden_size"]

    #create a file to write down for each random seed, the max validation accuracy and the corresponding average test accuracy
    temp_file_name = os.path.join(result_save_path,'validation_and_test_accuracy_each_random_seed.txt')
    auto_file = open(temp_file_name, 'w')

    #################### Initialize Indices for Validation (Early Stopping) ####################

    total_train_row = total_train_instances.shape[0]
    val_indices = list(range(total_train_row))
    if total_train_row > 1500:
        val_indices_count = 500
    else:
        val_indices_count = int (total_train_row / 3)
    val_indices = val_indices[-1 * val_indices_count:]

    # Provide a list of random seeds
    # Random_seed_list = [0, 1, 2, 3, 4]
    random_seed_list = [0]

    ########################### Initialize Log List ########################
    iteration_train_loss_for_different_person_list = [] #each element is the experiment for a person
    iteration_val_accuracy_for_different_person_list = [] #each element is the experiment for a person
    iteration_lr_for_different_person_list = [] #each element is the experiment for a person
    epoch_train_loss_for_different_person_list = [] #each element is the experiment for a person

    '''
    test_prediction_for_different_person_list = [] #each element is the experiment for a person
    test_label_for_different_person_list = [] #each element is the experiment for a person
    test_accuracy_for_different_person_list = [] #each element is the experiment for a person
    test_logit_for_different_person_list = [] #JUNE12: each element is the experiment for a person
    ensemble_test_logit_for_different_person_list = [] #July5: each element is the experiment for a person
    '''

    #################################### People Best Models #####################################
    people_best_models = []

    ########################### Train Model Using Best Hyper Parameter ########################
    #for idx, (train_file, test_file) in enumerate(zip(train_files, test_files)):
    for idx in list(range(group_count)):
        auto_file.write("#######################person: {}########################\n\n".format(idx+1))
        
        iteration_train_loss_for_this_person_list = [] #each element is the experiment for a random seed
        iteration_train_normal_loss_for_this_person_list = [] #each element is the experiment for a random seed        
        iteration_train_regularization_loss_for_this_person_list = [] #each element is the experiment for a random seed    
        iteration_val_accuracy_for_this_person_list = [] #each element is the experiment for a random seed
        iteration_lr_for_this_person_list = [] #each element is the experiment for a random seed
        epoch_train_loss_for_this_person_list = [] #each element is the experiment for a random seed

        #################################### Person Best Model #####################################
        person_best_model = None


        for random_seed in random_seed_list:
                        
            auto_file.write("random_seed: {}\n".format(random_seed))

            #setting random seed 
            torch.manual_seed(random_seed)
           
            #Train/Val get split indices
            print('current experiment using val_indices: {}'.format(val_indices))
            train_indices = [i for i in range(total_train_instances.shape[0]) if i not in val_indices]

            # Get Train Data
            train_instances = total_train_instances[train_indices]
            print(total_train_labels)
            train_labels = total_train_labels[train_indices]
            train_set = personal_brain_data(train_instances, train_labels)
            #Dataloader
            train_loader = torch.utils.data.DataLoader(train_set, batch_size = train_batch_size, shuffle = True)

            # Get Validation Data
            val_instances = total_train_instances[val_indices]
            val_labels = total_train_labels[val_indices]
            val_set = personal_brain_data(val_instances, val_labels)
            val_loader = torch.utils.data.DataLoader(val_set, batch_size = val_batch_size, shuffle = False)

            # Instanciate model:
            if model_class == 'SimpleRNN' or model_class == 'LSTM':
                model = model_to_use(input_size, hidden_size, num_layers, num_classes, num_directions, device).to(device)
                
            if model_class == 'LogisticRegression':
                model = model_to_use(input_size, num_classes).to(device)
            
            if model_class == 'CNN':
                model = model_to_use(input_size, conv1d_hidden_size, window_size, window_stride , linear_hidden_size, num_classes).to(device)

            
            #write down model info (layers and number of parameters etc)
            write_model_info(model.state_dict(), result_save_path, 'model_info.txt') #this line is inefficient. Every loop will overwrite the previous

            #Loss function and optimizer 
            criterion = nn.CrossEntropyLoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
            
            #Training loop
            # training_start_time = time.time()
            
            #for every person, re-initialize the epoch_train_loss_list and epoch_val_accuracy_list
            iteration_train_loss_list = None
            iteration_train_normal_loss_list = None
            iteration_train_regularization_loss_list = None
            iteration_val_accuracy_list = []
            iteration_lr_list = None
            epoch_train_loss_list = []
            
            best_val_accuracy = 0
            global_step = 0

            ################ Train start this person this random seed #########################
            for epoch in range(n_epoch):
                epoch_total_loss = 0.
                for i, (inputs, labels) in enumerate(train_loader):
                    global_step += 1
                    
                    average_minibatch_loss, this_epoch_iteration_lr_list, this_epoch_iteration_train_loss_list, this_epoch_iteration_train_normal_loss_list, this_epoch_iteration_train_regularization_loss_list = train_model(model, optimizer, criterion, train_loader, best_LAMBDA, device, model_class, train_only_last_layer=False)
            
                    if iteration_train_loss_list is None:
                        iteration_train_loss_list = this_epoch_iteration_train_loss_list
                    else:
                        iteration_train_loss_list = np.concatenate((iteration_train_loss_list, this_epoch_iteration_train_loss_list))

                    if iteration_train_normal_loss_list is None:
                        iteration_train_normal_loss_list = this_epoch_iteration_train_normal_loss_list
                    else:
                        iteration_train_normal_loss_list = np.concatenate((iteration_train_normal_loss_list, this_epoch_iteration_train_normal_loss_list))

                    if iteration_train_regularization_loss_list is None:
                        iteration_train_regularization_loss_list = this_epoch_iteration_train_regularization_loss_list
                    else:
                        iteration_train_regularization_loss_list = np.concatenate((iteration_train_regularization_loss_list, this_epoch_iteration_train_regularization_loss_list))

                    if iteration_lr_list is None:
                        iteration_lr_list = this_epoch_iteration_lr_list
                    else:
                        iteration_lr_list = np.concatenate((iteration_lr_list, this_epoch_iteration_lr_list))


                    if global_step % eval_every_iteration == 0:
                        validation_accuracy, _, _, _ = eval_model(model, val_loader, device, model_class)

                        iteration_val_accuracy_list.append(validation_accuracy)

                        if best_val_accuracy == 0 or validation_accuracy > best_val_accuracy:
                            print('epoch {}, loader index {}, current validation acc {}'.format(epoch, i, validation_accuracy))
                            print('\n\n--------------update the best model----------------')
                            best_val_accuracy = validation_accuracy

                            torch.save(model.state_dict(), os.path.join(result_save_path, 'person_' + str(idx+1)+ '_seed_'+ str(random_seed) +'_best_model' + '.statedict'))

                epoch_train_loss_list.append(average_minibatch_loss)

            
            ##write down the best validation accuracy for this random seed:
            auto_file.write("seed{} after finetuning, max validation accuracy: {}\n".format(random_seed, best_val_accuracy))

            epoch_train_loss_for_this_person_list.append(epoch_train_loss_list)
            iteration_train_loss_for_this_person_list.append(iteration_train_loss_list)
            iteration_train_normal_loss_for_this_person_list.append(iteration_train_normal_loss_list)        
            iteration_train_regularization_loss_for_this_person_list.append(iteration_train_regularization_loss_list)
            iteration_val_accuracy_for_this_person_list.append(iteration_val_accuracy_list)
            iteration_lr_for_this_person_list.append(iteration_lr_list)
    
            ################ Train finish this person this random seed #########################

            ################ Test start this person this random seed #########################

            load_model_path = os.path.join(result_save_path, 'person_' + str(idx+1)+ '_seed_'+ str(random_seed) + '_best_model' + '.statedict')
            
            if model_class == 'SimpleRNN' or model_class == 'LSTM':
                best_model = model_to_use(input_size, hidden_size, num_layers, num_classes, num_directions, device).to(device)
                
            if model_class == 'LogisticRegression':
                best_model = model_to_use(input_size, num_classes).to(device)
            
            if model_class == 'CNN':
                best_model = model_to_use(input_size, conv1d_hidden_size, window_size, window_stride , linear_hidden_size, num_classes).to(device)

            best_model.load_state_dict(torch.load(load_model_path))
            best_model.eval()

            ##################### Save the best model for this random seed as best model for this person ########################
            print("------------------------------------------------------------------------\n\n")
            print("Person {}, Random Seed {}, Best Model Trained".format(idx, random_seed))
            print("\n\n------------------------------------------------------------------------")
            person_best_model = best_model

        people_best_models.append(person_best_model)

        ########################### Append info for this person ########################
        iteration_train_loss_for_different_person_list.append(iteration_train_loss_for_this_person_list) #each element is the experiment for a random seed
        iteration_val_accuracy_for_different_person_list.append(iteration_val_accuracy_for_this_person_list) #each element is the experiment for a random seed
        epoch_train_loss_for_different_person_list.append(epoch_train_loss_for_this_person_list) #each element is the experiment for a random seed
        iteration_lr_for_different_person_list.append(iteration_lr_for_this_person_list) #each element is the experiment for a random seed

    ########################### Pack the log dict to return ########################
    log_dict = dict()
    
    log_dict["iteration_train_loss_for_different_person_list"] = iteration_train_loss_for_different_person_list
    log_dict["iteration_val_accuracy_for_different_person_list"] = iteration_val_accuracy_for_different_person_list
    log_dict["epoch_train_loss_for_different_person_list"] = epoch_train_loss_for_different_person_list
    log_dict["iteration_lr_for_different_person_list"] = iteration_lr_for_different_person_list

    return log_dict, people_best_models


def save_log_list(result_save_path, log_dict):
    
    iteration_train_loss_for_different_person_list = log_dict["iteration_train_loss_for_different_person_list"]
    iteration_val_accuracy_for_different_person_list = log_dict["iteration_val_accuracy_for_different_person_list"]
    epoch_train_loss_for_different_person_list = log_dict["epoch_train_loss_for_different_person_list"]
    iteration_lr_for_different_person_list = log_dict["iteration_lr_for_different_person_list"]
    
    #finally save the statistics
    pickle_to_file(os.path.join(result_save_path, 'iteration_train_loss_for_different_person_list.pkl'), iteration_train_loss_for_different_person_list)
    pickle_to_file(os.path.join(result_save_path, 'iteration_val_accuracy_for_different_person_list.pkl'), iteration_val_accuracy_for_different_person_list)
    pickle_to_file(os.path.join(result_save_path, 'epoch_train_loss_for_different_person_list.pkl'), epoch_train_loss_for_different_person_list)
    pickle_to_file(os.path.join(result_save_path, 'iteration_lr_for_different_person_list.pkl'), iteration_lr_for_different_person_list)


def train_model(model, optimizer, criterion, train_loader, L2_LAMBDA, device, model_class, train_only_last_layer = False):
    model.train()
    
    # freeze all parameters except last layer (logistic regression only has 0 layer):
    if model_class != 'LogisticRegression':
        if train_only_last_layer: 
            for param in model.parameters():
                param.requires_grad = False

            model.fc.weight.requires_grad=True
            model.fc.bias.requires_grad=True
        
        
    epoch_total_loss = 0.
    
    iteration_lr_list = []
    iteration_train_loss_list = []
    iteration_train_normal_loss_list = []
    iteration_train_regularization_loss_list = []
    for i, (inputs, labels) in enumerate(train_loader):
        if model_class == 'LogisticRegression':
            inputs = torch.mean(inputs, dim = 1)

        #put data to device
        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        #forward pass
        outputs = model(inputs)
        #calculate loss
        loss = criterion(outputs, labels)
        
        #https://sebastianraschka.com/pdf/lecture-notes/stat479ss19/L10_regularization_slides.pdf
        # regularize loss
        L2 = 0.
        for p in model.parameters():
            L2 = L2 + (p**2).sum()
        
        regularization_loss = 2./labels.size(0) * L2_LAMBDA * L2
        
        total_loss = loss + regularization_loss

        #calculate gradient
        total_loss.backward()
        #perform parameters update
        optimizer.step()

        current_lr = [group['lr'] for group in optimizer.param_groups][0] #general way to get current lf. didn't specify different para group for different lr
        iteration_lr_list.append(current_lr)

        current_minibatch_loss = total_loss.item() #is already per sample loss
        iteration_train_loss_list.append(current_minibatch_loss)
        epoch_total_loss += current_minibatch_loss
        
        iteration_train_normal_loss_list.append(loss.item())
        iteration_train_regularization_loss_list.append(regularization_loss.item())
        
    
    average_minibatch_loss = epoch_total_loss/len(train_loader) #how many batches
    
    return average_minibatch_loss, iteration_lr_list, iteration_train_loss_list, iteration_train_normal_loss_list, iteration_train_regularization_loss_list

def log_total_time(logger_confusion_matrix, program_start_time):
    #log total run time     
    program_end_time = time.time()
    
    logger_confusion_matrix.log('total program run-time: {}'.format(program_end_time - program_start_time))
    logger_confusion_matrix.flush()

def load_train_data(train_dir, train_files, load_mode, col_index, feature_index):
    # load_mode: personal, group
    if load_mode == "personal":
        total_train_instances, total_train_labels = read_data_single(os.path.join(train_dir, train_files[0]), col_index, feature_index)
        # print("------------------------------------\n\n")
        # print("load_train_data type and shape")
        # print("type:")
        # print(type(total_train_instances))
        # print("shape")
        # print(total_train_instances.shape)
        # print("\n\n------------------------------------")
    elif load_mode == "group":
        total_train_instances = None
        total_train_labels = None
    return total_train_instances, total_train_labels

def predict_chunk_test_data(test_set, people_best_models, param_dict):
    #################### Initialize cuda device setting ####################
    test_batch_size = param_dict["test_batch_size"]
    person_index = param_dict["person_index"]
    model_class = param_dict["model_class"]
    
    test_loader = torch.utils.data.DataLoader(test_set, batch_size = test_batch_size, shuffle = False)

    cuda = torch.cuda.is_available()
    if cuda:
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

    model = people_best_models[person_index]

    predicted_label = eval_model_single_chunk(model, test_loader, device, model_class = model_class)
    return predicted_label

