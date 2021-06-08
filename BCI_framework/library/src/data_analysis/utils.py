import pickle
import time
import numpy as np
import torch
import csv 
import os
# from matplotlib import gridspec
# import matplotlib.pyplot as plt

#June15: plot scatter plot of the 
def plot_test_performance_lineplot(test_accuracy_for_different_person_list, test_performance_lineplot_save_dir='./'):
    
    #     num_trial = len(random_seed_test_accuracy_lists)
    num_person = len(test_accuracy_for_different_person_list)
    num_trial = len(test_accuracy_for_different_person_list[0])
    
    #restructure the list format
    random_seed_0_accuracy = [i[0] for i in test_accuracy_for_different_person_list]
    random_seed_1_accuracy = [i[1] for i in test_accuracy_for_different_person_list]
    random_seed_2_accuracy = [i[2] for i in test_accuracy_for_different_person_list]
    random_seed_3_accuracy = [i[3] for i in test_accuracy_for_different_person_list]
    random_seed_4_accuracy = [i[4] for i in test_accuracy_for_different_person_list]
    
    random_seed_test_accuracy_lists = [random_seed_0_accuracy, random_seed_1_accuracy, random_seed_2_accuracy, random_seed_3_accuracy, random_seed_4_accuracy]

    
    plt.figure(figsize = (10,6))
    plt.title('Test accuracy across run and person')
    
    color_dict = {0:'green', 1:'red', 2:'yellow', 3:'blue', 4:'magenta'}

    for i in range(num_trial):
        plt.plot(np.array(range(len(random_seed_test_accuracy_lists[i]))), random_seed_test_accuracy_lists[i], color = color_dict[i], label = 'random_seed_' + str(i))
        plt.scatter(np.array(range(len(random_seed_test_accuracy_lists[i]))), random_seed_test_accuracy_lists[i], marker='^', c = 'black')

    plt.xticks(np.arange(0, 26, 1))
    plt.xlabel('person')
    plt.ylabel('Test accuracy')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.9))
    
    save_fig_path = test_performance_lineplot_save_dir + 'test_performance_accross_runs_lineplot.png'
    plt.savefig(save_fig_path)
    plt.close()

#June15: writing model information:
def write_model_info(model_state_dict, result_save_path, file_name):
    temp_file_name = os.path.join(result_save_path, file_name)
    
    auto_file = open(temp_file_name, 'w')
    total_elements = 0
    for name, tensor in model_state_dict.items():
        total_elements += torch.numel(tensor)
        auto_file.write('\t Layer {}: {} elements \n'.format(name, torch.numel(tensor)))

        #print('\t Layer {}: {} elements'.format(name, torch.numel(tensor)))
    auto_file.write('\n total elemets in this model state_dict: {}\n'.format(total_elements))
    #print('\n total elemets in this model state_dict: {}\n'.format(total_elements))
    auto_file.close()    

def pickle_to_file(file_name, data, protocol = pickle.HIGHEST_PROTOCOL):
    with open(file_name, 'wb') as handle:
        pickle.dump(data, handle, protocol)

def process_with_sliding_window(instances, labels):
    '''
    each chunk contain 765 rows. 
    instances is of shape (#chunk, #rows_per_chunk, #features)
    '''
    #each chunk is expanded 11 times
    #     chunk_length = 765
    #     local_step_size = 60
    #     local_window_size = 165

    processed_instance_list = []
    processed_label_list = []
    
    #hard coded: start_indexes: [0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600]
    #hard coded: end_indexes:   [165, 225, 285, 345, 405, 465, 525, 585, 645, 705, 765]
    start_indexes = [i * 60 for i in range(11)]
    end_indexes = [i + 165 for i in start_indexes] 
    
    number_of_chunks = instances.shape[0]
    print('{} chunks the passed into sliding window function'.format(number_of_chunks))
    
    for chunk_id in range(number_of_chunks):
        for start, end in zip(start_indexes, end_indexes):
            processed_instance_list.append(instances[chunk_id][start:end])
            processed_label_list.append(labels[chunk_id])
            
    
    processed_instance_list = np.array(processed_instance_list, dtype=np.float32) 
    processed_label_list = np.array(processed_label_list, dtype=np.int64)
    
    return processed_instance_list, processed_label_list 

def eval_model_single_chunk(model, eval_loader, device, model_class = 'LogisticRegression'):
    # Test the Model
    model.eval()

    for chunk_df in eval_loader: #test_loader

        if model_class == 'LogisticRegression':
            chunk_df = torch.mean(chunk_df, dim = 1)
            
        chunk_df = chunk_df.to(device)

        outputs = model(chunk_df)
        
        _, predicted = torch.max(outputs.data, 1)

    return predicted.data.cpu().numpy()[0]

def eval_model(model, eval_loader, device, model_class = 'LogisticRegression'):
    # Test the Model
    model.eval()

    eval_start_time = time.time()
    #print('>>>>>>>>>>>>>>>>>>>>>>>>>>Start Evaluation:', flush = True)
    correct = 0.0
    total = 0.0
    predicted_list = []
    label_list = []
    logit_list = [] #JUNE12
    for inputs, labels in eval_loader:#test_loader
        #inputs = inputs.view(-1, sequence_length, input_size)
        if model_class == 'LogisticRegression':
            inputs = torch.mean(inputs, dim = 1)
       
            
        inputs = inputs.to(device)

        outputs = model(inputs)
        logit_list.append(outputs.data.cpu().numpy()) #JUNE12
        #print('after outputs.data.cpu(), outputs is still on gpu: {}'.format(outputs.is_cuda))
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        
        for p, l in zip(predicted, labels):
            predicted_list.append(p.item())
            label_list.append(l.data.numpy())#June12
            if p.item() == l:
                correct += 1.0
    
    accuracy = correct / total
    eval_end_time = time.time()

    #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>Finished Evaluation, evaluation time: {}'.format(eval_end_time - eval_start_time), flush = True)
    
    return accuracy, predicted_list, label_list, logit_list #JUNE12

def write_stats_csv(test_accuracy_for_different_person_list, result_save_dir):

    # Write results onto disk.
    with open(os.path.join(result_save_dir, 'test_accuracy_stats.csv'), 'wt', encoding='utf-8') as f:
        f = csv.writer(f)
        f.writerow(['person','max_accuracy', 'min_accuracy', 'avg_accuracy', 'std'])    
        for person_id in range(len(test_accuracy_for_different_person_list)):
            f.writerow([str(person_id + 1), round(np.max(np.array(test_accuracy_for_different_person_list[person_id])),3), round(np.min(np.array(test_accuracy_for_different_person_list[person_id])),3), round(np.mean(np.array(test_accuracy_for_different_person_list[person_id])),3), round(np.std(np.array(test_accuracy_for_different_person_list[person_id])),3)])

def plot_test_performance_bar(random_seed_list, test_accuracy_for_different_person_list, test_performance_bar_save_dir='./'):
    num_trial = len(random_seed_list)

    #     fig, axes = plt.subplots(2, 7) #want two row, total 14 person is fixed
    fig, axes = plt.subplots(4, 7) #want two row, total 14 person is fixed
    fig.subplots_adjust(hspace = 0.3, wspace = 0.5)
    fig.set_size_inches(32.5, 14.5)
    fig.suptitle('Test Accuracy Across Runs', fontsize=16)
    
    position = np.arange(num_trial)
    objects = ['seed_' + str(i) for i in random_seed_list]
    ylabel = 'test_accuracy'

    for i, ax in enumerate(axes.flat):
        # Plot image.
        if i == 26 or i == 27:
            continue
        average_accuracy = round(np.mean(np.array(test_accuracy_for_different_person_list[i])),3)
        standard_deviation = round(np.std(np.array(test_accuracy_for_different_person_list[i])),4)

        ax.bar(position, test_accuracy_for_different_person_list[i], label = 'average accuracy: ' + str(average_accuracy) + '\n std: ' + str(standard_deviation))
        title = 'person_' + str(i)   
        ax.set_ylabel(ylabel)
        ax.set_ylim(bottom=0, top=1)
        ax.set_title(title)
        ax.set_xticks(position)
        ax.set_xticklabels(objects, rotation=30)
        ax.legend()


    save_fig_path = test_performance_bar_save_dir + 'test_performance_accross_runs.png'
    plt.savefig(save_fig_path)
    plt.close()

def plot_train_val_loss(random_seed_list, iteration_train_loss_for_different_person_list, iteration_val_accuracy_for_different_person_list, eval_every_iteration, learning_curve_result_save_dir='./'):
    '''
    For each random seed, plot the train/val loss vs step (default to use epoch as step) for each person
    
    random_seed_list: a list of random seeds
    random_seed_iteration_train_loss_list: a list of iteration_train_loss_list (each person)
    random_seed_iteration_val_accuracy_list: a list of val_accuracy_list (each person)
    
    '''
    
    
    num_trials = len(random_seed_list)
    num_persons = len(iteration_train_loss_for_different_person_list)
    
    for person_id in range(num_persons):
        iteration_train_loss_for_this_person_list = iteration_train_loss_for_different_person_list[person_id]
        iteration_val_accuracy_for_this_person_list = iteration_val_accuracy_for_different_person_list[person_id]
        
        for trial in range(num_trials):
            fig = plt.figure(figsize=(20,10))
            gs = gridspec.GridSpec(2,num_trials)

            ax1 = plt.subplot(gs[0,trial])
            ax1.plot(np.array(range(len(iteration_train_loss_for_this_person_list[trial]))), np.array(iteration_train_loss_for_this_person_list[trial]), '-b', label = 'train_loss')
            ax1.legend(loc='upper left')
            ax1.set_xlabel('iterations')
            

            ax2 = plt.subplot(gs[1,trial])
            ax2.plot(np.array(range(len(iteration_val_accuracy_for_this_person_list[trial]))), np.array(iteration_val_accuracy_for_this_person_list[trial]), '-b', label = 'val_accuracy')
            ax2.legend(loc='upper left')
            ax2.set_xlabel('iterations')
        
            save_fig_path = learning_curve_result_save_dir + 'person_' + str(person_id + 1) + '_seed'+ str(trial)+'.png'
            plt.savefig(save_fig_path)
        
        plt.close()

def plot_learning_rate_schedule(random_seed_list, iteration_lr_for_different_person_list, learning_rate_schedule_result_save_dir='./'):
    '''
    For each random seed, plot the learning rate vs step (default to use epoch as step) for each person
    
    random_seed_list: a list of random seeds
    random_seed_iteration_lr_lists: a list of iteration_lr_list (each person)
       
    '''
    
    num_trials = len(random_seed_list)
    num_persons = len(iteration_lr_for_different_person_list)
    
    for person_id in range(num_persons):
        iteration_lr_for_this_person_list = iteration_lr_for_different_person_list[person_id]
        
        for trial in range(num_trials):
            fig = plt.figure(figsize=(50,25))
            gs = gridspec.GridSpec(1,num_trials)

            ax1 = plt.subplot(gs[0,trial])
            ax1.plot(np.array(range(len(iteration_lr_for_this_person_list[trial]))), np.array(iteration_lr_for_this_person_list[trial]), '-b', label = 'lr')
            ax1.legend(loc='upper left')
            ax1.set_xlabel('iterations')
            ax1.set_title('seed {}'.format(trial))
            
        
        save_fig_path = learning_curve_result_save_dir + 'person_' + str(person_id + 1) + 'LR_schedule.png'
        plt.savefig(save_fig_path)
        plt.close()
