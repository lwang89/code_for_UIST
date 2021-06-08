## Description: Read fNIRS data

from torch.utils.data import Dataset
import pandas as pd
import numpy as np
import glob


class brain_dataset(Dataset):

    def __init__(self, instance_list, label_list):
        self.instance_list = instance_list
        self.instance_label = label_list
           
    def __getitem__(self, index):
        return self.instance_list[index], self.instance_label[index]
    
    def __len__(self):
        return len(self.instance_list)
    
    def __get_instance_label__(self):
        return self.instance_label
    
    def __get_instance_list__(self):
        return np.array(self.instance_list).shape
    
    
def read_subject_csv(path, select_feature_columns = ['AB_I_O', 'AB_PHI_O', 'AB_I_DO', 'AB_PHI_DO',\
                                                    'CD_I_O', 'CD_PHI_O', 'CD_I_DO', 'CD_PHI_DO'],\
                    label_list = [0, 2]):
    
    '''
    path: path to the csv file
    '''
    
    instance_list = []
    instance_label = []

    label_dict = dict()
    for i in range(len(label_list)):
        label = label_list[i]
        label_dict[label] = i
    
    # each subject csv file contain 2224 chunks (segments)
    subject_df = pd.read_csv(path)
    total_chunk_count = np.max(subject_df.chunk.values) + 1
    # assert np.max(subject_df.chunk.values) + 1 == total_chunk_count, '{} does not have 2224 chunks'.format(path) 

    subject_df = subject_df[select_feature_columns + ['chunk'] + ['label']] #JUNE11

    # segment id: 0 to 2223
    for i in range(0, total_chunk_count):
        # select feature values if the current chunk
        chunk_matrix = subject_df.iloc[:,:-2].loc[subject_df['chunk'] == i].values
        # select label values of the current chunk
        label_for_this_segment = subject_df[subject_df['chunk'] == i].label.values[0]

        if label_for_this_segment in label_list:
            instance_list.append(chunk_matrix)
            instance_label.append(label_dict[label_for_this_segment])

    instance_list = np.array(instance_list, dtype=np.float32) 
    instance_label = np.array(instance_label, dtype=np.int64)
    
    # print(instance_label.shape)
    return instance_list, instance_label