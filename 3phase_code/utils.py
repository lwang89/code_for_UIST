## Description: includding the data augmentation method MixUp and some other methods used while building the model.

import pickle
import time
import numpy as np
import torch
import csv 
import os
import random
import logging
import shutil
import torch.nn.functional as F
import json

from matplotlib import gridspec
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix as sklearn_cm
import seaborn as sns

def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True


def makedir_if_not_exist(specified_dir):
    if not os.path.exists(specified_dir):
        os.makedirs(specified_dir)


def convert_numpyarray_to_onehot(input_array, class_number=4):
    # 0back, 1back, 2back, 3back
    onehot_encoding = np.eye(class_number)[input_array]
    
    return onehot_encoding


def MixUp_expansion(prior_sub_feature_array, prior_sub_label_array, alpha = 0.75, expand=2):
    
    '''
    Mixing strategy1: mixing same chunk of different person to create synthetic person
                      randomly choose two person, sample lambda from beta distribution, use the same beta for each chunk
    '''
    # Make sure same number of subjects
    assert len(prior_sub_feature_array) == len(prior_sub_label_array)
    assert isinstance(prior_sub_feature_array, np.ndarray), 'input_images is not numpy array'
    assert isinstance(prior_sub_label_array, np.ndarray), 'input_labels is not numpy array'

    expanded_sub_feature_array = None
    expanded_sub_label_array = None
    
    num_sub = len(prior_sub_feature_array)
    
    for i in range(expand):
        # generate a different random lambda value for each subject
        lam = np.random.beta(alpha, alpha, (num_sub, 1, 1, 1))
        lam = np.maximum(lam, (1 - lam)) #ensure the created samples is closer to the first sample

        permutation_indices = np.random.permutation(num_sub)

        #linear interpolation of features
        synthetic_sub_feature_array = prior_sub_feature_array * lam + prior_sub_feature_array[permutation_indices] * (1 - lam)

        #linear interpolation of labels
        synthetic_sub_label_array = prior_sub_label_array * lam[:, :, :, 0] + prior_sub_label_array[permutation_indices] * (1 - lam[:, :, :, 0])  

        if expanded_sub_feature_array is None:
            expanded_sub_feature_array = synthetic_sub_feature_array
            expanded_sub_label_array = synthetic_sub_label_array
        else:     
            expanded_sub_feature_array = np.concatenate((expanded_sub_feature_array, synthetic_sub_feature_array))
            expanded_sub_label_array = np.concatenate((expanded_sub_label_array, synthetic_sub_label_array))
    
    return expanded_sub_feature_array, expanded_sub_label_array


#for pytorch, need to define soft cross entropy (no built-in supported)
#https://discuss.pytorch.org/t/soft-cross-entropy-loss-tf-has-it-does-pytorch-have-it/69501
def soft_cross_entropy(logits, soft_target):
    '''
    soft_target: e.g., [0.1, 0.2, 0.6, 0.1]
    '''
    logprobs = F.log_softmax(logits, dim=1)
    soft_cross_entropy_loss = -(soft_target * logprobs).sum()/logits.shape[0]
   
    return soft_cross_entropy_loss


def train_one_epoch(model, optimizer, criterion, train_loader, device, model_class):
    model.train()
    
    loss_avg = RunningAverage()
    for i, (data_batch, onehot_labels_batch) in enumerate(train_loader):
        if model_class == 'LogisticRegression':
            data_batch = torch.mean(data_batch, dim = 1) #torch.Size([batch_size, num_features])

        data_batch = data_batch.to(device) #put inputs to device
        onehot_labels_batch = onehot_labels_batch.to(device) #when performing training, need to also put labels to device to do loss calculation and backpropagation

        #forward pass
        #outputs: tensor on gpu, requires grad, torch.Size([batch_size, num_classes])
        output_batch = model(data_batch)
        
        #calculate loss
        #loss: tensor (scalar) on gpu, torch.Size([])
        loss = criterion(output_batch, onehot_labels_batch)
        
        #update running average of the loss
        loss_avg.update(loss.item())
        
        #clear previous gradients
        optimizer.zero_grad()

        #calculate gradient
        loss.backward()

        #perform parameters update
        optimizer.step()
    
    average_loss_this_epoch = loss_avg()
    return average_loss_this_epoch


class RunningAverage():
    '''
    A class that maintains the running average of a quantity
    
    Usage example:
    loss_avg = RunningAverage()
    loss_avg.update(2)
    loss_avg.update(4)
    
    '''

    def __init__(self):
        self.steps = 0
        self.total = 0
    
    def update(self, val):
        self.total += val
        self.steps += 1
    
    def __call__(self):
        return self.total / float(self.steps)


def eval_model(model, eval_loader, device, model_class = 'LogisticRegression'):
    
    #reference: https://github.com/cs230-stanford/cs230-code-examples/blob/master/pytorch/nlp/evaluate.py
    #set the model to evaluation mode
    model.eval()

    
    # predicted_array = None # 1d numpy array, [batch_size * num_batches]
    onehot_labels_array = None # 1d numpy array, [batch_size * num_batches]
    logits_array = None # 2d numpy array, [batch_size * num_batches, num_classes] 
    
    for data_batch, onehot_labels_batch in eval_loader:#test_loader          
        if model_class == 'LogisticRegression':
            data_batch = torch.mean(data_batch, dim = 1) #torch.Size([batch_size, num_features])
       
            
        data_batch = data_batch.to(device) #put inputs to device

        #forward pass
        #outputs: tensor on gpu, requires grad, torch.Size([batch_size, num_classes])
        output_batch = model(data_batch)
        
        #extract data from torch variable, move to cpu, convert to numpy arrays    
        if onehot_labels_array is None:
            onehot_labels_array = onehot_labels_batch.data.cpu().numpy()
            
        else:
            onehot_labels_array = np.concatenate((onehot_labels_array, onehot_labels_batch.data.cpu().numpy()), axis=0)#np.concatenate without axis will flattened to 1d array
        
        
        if logits_array is None:
            logits_array = output_batch.data.cpu().numpy()
        else:
            logits_array = np.concatenate((logits_array, output_batch.data.cpu().numpy()), axis = 0) #concatenate on batch dimension: torch.Size([batch_size * num_batches, num_classes])
            
    class_predictions_array = logits_array.argmax(1)
    class_labels_array = onehot_labels_array.argmax(1)
    
    accuracy = (class_predictions_array == class_labels_array).mean() * 100
    
    
    return accuracy, class_predictions_array, class_labels_array, logits_array


def save_training_curves(figure_name, result_save_subject_trainingcurvedir, epoch_train_loss, epoch_validation_accuracy = None):
    
    fig = plt.figure(figsize=(15, 8))
    
    ax_1 = fig.add_subplot(1,2,1)
    ax_1.plot(range(len(epoch_train_loss)), epoch_train_loss, label='epoch_train_loss')
    
    if epoch_validation_accuracy is not None:
        ax_2 = fig.add_subplot(1,2,2, sharex = ax_1)
        ax_2.plot(range(len(epoch_validation_accuracy)), epoch_validation_accuracy, label='epoch_validation_accuracy')
        ax_2.legend()
    
    ax_1.legend()
        
    figure_save_path = os.path.join(result_save_subject_trainingcurvedir, figure_name)
    plt.savefig(figure_save_path)
    plt.close()

def save_training_curves_json(figure_name, result_save_subject_trainingcurvedir, epoch_train_loss, epoch_validation_accuracy = None):
    json_save_path = os.path.join(result_save_subject_trainingcurvedir, figure_name)

    value_dict = dict()
    value_dict['figure_name'] = figure_name
    value_dict['result_save_subject_trainingcurvedir'] = result_save_subject_trainingcurvedir
    value_dict['epoch_train_loss'] = epoch_train_loss

    if epoch_validation_accuracy is not None:
        value_dict['epoch_validation_accuracy'] = epoch_validation_accuracy
    
    # save file
    with open(json_save_path, 'w') as outfile:
        json.dump(value_dict, outfile)

def plot_confusion_matrix(predictions, true_labels, figure_labels, result_save_subject_resultanalysisdir, output_filename, normalized_option = None):
    """Plot confusion matrix using heatmap.
 
    Args:
        data (list of list): List of lists with confusion matrix data.
        labels (list): Labels which will be plotted across x and y axis.
        output_filename (str): Path to output file.
 
    """
    sns.set(color_codes=True)
    plt.figure(1, figsize=(8, 5))
 
    plt.title("Confusion Matrix")
    
    data = sklearn_cm(true_labels, predictions)
    print('Inside plot_confusion_matrix, data is {}'.format(data), flush = True)

    sns.set(font_scale=1.4)
    if normalized_option == 'Recall':
        data = data.astype(np.float16)
        data[0] = data[0]/np.sum(data[0])
        data[1] = data[1]/np.sum(data[1])
        data[2] = data[2]/np.sum(data[2])
        data[3] = data[3]/np.sum(data[3])
        ax = sns.heatmap(data, annot=True, 
            fmt='.01%', cmap='Blues')
        
    elif normalized_option == 'Error':
        data = data.astype(np.float16)
        np.fill_diagonal(data, 0)
        data = data/np.sum(data)
        ax = sns.heatmap(data, annot=True, 
            fmt='.01%', cmap='Blues')
 
    else:
        ax = sns.heatmap(data, annot=True, 
            fmt='d', cmap='Blues')
    
    ax.set_xticklabels(figure_labels)
    ax.set_yticklabels(figure_labels)
 
    ax.set(ylabel="True Label", xlabel="Predicted Label")
    ax.set_ylim([4, 0])

    plt.savefig(os.path.join(result_save_subject_resultanalysisdir, output_filename), bbox_inches='tight', dpi=300)
    plt.close()

def plot_confusion_matrix_json(predictions, true_labels, figure_labels, result_save_subject_resultanalysisdir, output_filename, normalized_option = None):
    json_save_path = os.path.join(result_save_subject_resultanalysisdir, output_filename)

    value_dict = dict()
    value_dict['predictions'] = predictions.tolist()
    value_dict['true_labels'] = true_labels.tolist()
    value_dict['figure_labels'] = figure_labels
    value_dict['result_save_subject_resultanalysisdir'] = result_save_subject_resultanalysisdir
    value_dict['output_filename'] = output_filename

    if normalized_option is not None:
        value_dict['normalized_option'] = normalized_option
    
    # save file
    with open(json_save_path, 'w') as outfile:
        json.dump(value_dict, outfile)

def ensemble_and_extract_performance(model_state_dict, result_save_subject_predictionsdir, result_save_subject_resultanalysisdir):
    '''
    used for extracting performance for phase3 model
    '''
    
    #create file writer
    file_writer = open(os.path.join(result_save_subject_resultanalysisdir, 'performance.txt'), 'w')
    
    #load saved test predictions
    CV_predictions_dict = load_pickle(result_save_subject_predictionsdir, 'phase3_save_dict.pkl')
    
    assert np.array_equal(CV_predictions_dict['fold0_bestepoch_test_class_labels'], CV_predictions_dict['fold1_bestepoch_test_class_labels']) and np.array_equal(CV_predictions_dict['fold1_bestepoch_test_class_labels'], CV_predictions_dict['fold2_bestepoch_test_class_labels']) and np.array_equal(CV_predictions_dict['fold2_bestepoch_test_class_labels'], CV_predictions_dict['fold3_bestepoch_test_class_labels']) and np.array_equal(CV_predictions_dict['fold3_bestepoch_test_class_labels'], CV_predictions_dict['fold4_bestepoch_test_class_labels']), 'test set should not shuffle'
    
    
    #perform ensemble
    predictions_to_ensemble = [CV_predictions_dict['fold{}_bestepoch_test_logits'.format(i)] for i in range(5)]
    true_labels = CV_predictions_dict['fold0_bestepoch_test_class_labels']
    
    bagging_accuracy = simple_bagging(predictions_to_ensemble, true_labels)
    
    average_cv_validation_accuracy = np.mean(np.array([CV_predictions_dict['fold{}_bestepoch_val_accuracy'.format(i)] for i in range(5)]))
    #write performance to file
    file_writer.write('Average cv validation accuracy: {}\n\n'.format(average_cv_validation_accuracy))

    
    file_writer.write('Test accuracy:\n')
    file_writer.write('fold0: {}\n'.format(CV_predictions_dict['fold0_bestepoch_test_accuracy']))
    file_writer.write('fold1: {}\n'.format(CV_predictions_dict['fold1_bestepoch_test_accuracy']))
    file_writer.write('fold2: {}\n'.format(CV_predictions_dict['fold2_bestepoch_test_accuracy']))
    file_writer.write('fold3: {}\n'.format(CV_predictions_dict['fold3_bestepoch_test_accuracy']))
    file_writer.write('fold4: {}\n\n'.format(CV_predictions_dict['fold4_bestepoch_test_accuracy']))
    file_writer.write('Ensemble_5folds: {}\n\n'.format(bagging_accuracy))
    
    #write model parameters to file
    file_writer.write('Model parameters:\n')

    total_elements = 0
    for name, tensor in model_state_dict.items():
        file_writer.write('layer {}: {} parameters\n'.format(name, torch.numel(tensor)))
        total_elements += torch.numel(tensor)
    file_writer.write('total elemets in this model: {}'.format(total_elements))
        

    return bagging_accuracy


def simple_bagging(predictions_to_ensemble, true_labels):
    
    running_predictions = 0
    for predictions in predictions_to_ensemble:
        print('predictions.shape: {}'.format(predictions.shape))
        running_predictions += predictions
    
    ensembled_class_predictions = running_predictions.argmax(1)
    ensembled_accuracy = (ensembled_class_predictions == true_labels).mean() * 100
    
    return ensembled_accuracy


def load_pickle(result_dir, filename):
    with open(os.path.join(result_dir, filename), 'rb') as f:
        data = pickle.load(f)
    
    return data


def save_pickle(save_dir, save_file_name, data):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    data_save_fullpath = os.path.join(save_dir, save_file_name)
    with open(data_save_fullpath, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


class Params():
    """Class that loads hyperparameters from a json file
    
    Example:
    '''
    params = Params(json_path)
    print(params.learning_rate)
    params.learning_rate = 0.5  # change the value of learning_rate in params
    '''
    """
    
    def __init__(self, json_path):
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)
    
    def save(self, json_path):
        with open(json_path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)
        
    def update(self, json_path):
        """Loads parameters from json file"""
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)
    
    @property
    def dict(self):
        """Gives dict-like access to Params instance by 'params.dict['learning_rate']'"""
        return self.__dict__


def set_logger(log_path):
    """Set the logger to log info in terminal and file 'log_path'.
    
    In general, it is useful to have a logger so that every output to the terminal is saved in a 
    permanent file. Here we save it to 'model_dir/train.log'
    
    Example:
    '''
    logging.info("Start training...")
    '''
    
    Args:
        log_path: (string) where to log
    """
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # Logging to a file
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
        logger.addHandler(file_handler)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(stream_handler)    


def save_dict_to_json(d, json_path):
    """Saves dict of floats in josn file
    
    Args:
        d: (dict) of float-castable values (np.float, int, float, etc.)
        json_path: (string) path to json file
    """
    with open(json_path, 'w') as f:
        d = {k: float(v) for k, v in d.items()}
        json.dump(d, f, indent=4)


def save_checkpoint(state, is_best, checkpoint):
    """Save model and training parameters at checkpoint + 'last.pth.tar'. If is_best==True, also saves checkpoint + 'best.pth.tar'
    
    Args:
        state: (dict) contains model's state_dict, may contain other keys such as epoch, optimizer state_dict
        is_best: (bool) True if it is the best model seen till now
        checkpoint: (string) folder where parameters are to be saved
    """
    
    filepath = os.path.join(checkpoint, 'last.pth.tar')
    if not os.path.exists(checkpoint):
        print("Checkpoint Directory does not exist! Making directory {}".format(checkpoint))
        os.mkdir(checkpoint)
    
    else:
        print("Checkpoint Directory exists!")
    
    torch.save(state, filepath)
    
    if is_best:
        shutil.copyfile(filepath, os.path.join(checkpoint, 'best.pth.tar'))


def load_checkpoint(checkpoint, model, optimizer=None):
    """Loads model parameters (state_dict) from file_path. 
    If optimizer is provided, loads state_dict of optimizer assuming it is present in checkpoint.
    
    Args:
        checkpoint: (string) filename which needs to be loaded
        model: model for which the parameters are loaded
        optimizer: (torch.optim) optional: resume optimizer from checkpoint
    """
    
    if not os.path.exists(checkpoint):
        raise("File doesn't exist {}".format(checkpoint))
    
    checkpoint = torch.load(checkpoint)
    model.load_state_dict(checkpoint['state_dict'])
    
    if optimizer:
        optimizer.load_state_dict(checkpoint['optim_dict'])
    
    return checkpoint

def write_model_info(model_state_dict, result_save_path, file_name):
    temp_file_name = os.path.join(result_save_path, file_name)
    
    auto_file = open(temp_file_name, 'w')
    total_elements = 0
    for name, tensor in model_state_dict.items():
        total_elements += torch.numel(tensor)
        auto_file.write('\t Layer {}: {} elements \n'.format(name, torch.numel(tensor)))

    auto_file.write('\n total elemets in this model state_dict: {}\n'.format(total_elements))
    auto_file.close()