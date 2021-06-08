#data set class

from torch.utils.data import Dataset
import pandas as pd
import numpy as np
import glob




class personal_brain_data(Dataset):

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
    
class personal_test_brain_data(Dataset):
    
    def __init__(self, instance_list):
        self.instance_list = instance_list
           
    def __getitem__(self, index):
        return self.instance_list[index]
    
    def __len__(self):
        return len(self.instance_list)
    
    def __get_instance_list__(self):
        return np.array(self.instance_list).shape

class group_brain_data(Dataset):

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
    
def read_data_single(path, col_index, feature_index):
    # global MUSE_col_index
    instance_list = []
    instance_label = []

    print("feature length is " , len(col_index))
    

    train_df = pd.read_csv(path) 
    #应该是在此处filter想要的column即可, 取column时从.iloc[:,2:-2]---> [:,:-2]
    # train_df = train_df[prefrontal_cols + ['N'] + ['chunk']] 
    train_df = train_df[col_index] 

    # print("all chunk numbers:")
    # print(train_df['chunk'])

    chunk_size = int(train_df['chunk'].max() + 1)

    print("number of chunks for train session: ", chunk_size)

    # Add label for each chunk
    for i in range(0, chunk_size):
        # Select the chunk
        chunk_matrix = train_df[feature_index].loc[train_df['chunk'] == i].values
        instance_list.append(chunk_matrix)
    
        # Get the label
        label_for_this_chunk = train_df[train_df['chunk'] == i].label.values[0]
        # print('label for this chunk is {}'.format(label_for_this_chunk))

        # Record the label
        instance_label.append(label_for_this_chunk)

            
    instance_list = np.array(instance_list, dtype=np.float32) 
    instance_label = np.array(instance_label, dtype=np.int64)
    
    return instance_list, instance_label



def read_data_group(phase, path, exclude_person = None):
    # load all the train csv files in the specified folder
    instance_list = []
    instance_label = []
    
    if phase == "train":
        allFiles = glob.glob(path + "/*.csv") #a list of string, each string is the file path
        
        #hz: Mar9: to accompany newly added arg 'exclude_person'---for implementing expanded_person_specific model, not for training on group and exclude some train files
        if exclude_person is not None:
            allFiles = [file for file in allFiles if exclude_person not in file]
            
        # each train csv file contain 21 chunks (chunks)
        for file_ in allFiles:
            print('loading file {}'.format(file_))
            train_df = pd.read_csv(file_)
            #应该是在此处filter想要的column即可，取column时从.iloc[:,2:-2]---> [:,:-2]
            prefrontal_cols = [col for col in train_df if 'AF' in col] #JUNE11
            train_df = train_df[prefrontal_cols + ['N'] + ['chunk']] #JUNE11
            #train chunk id start from 0 to 20
            for i in range(0, 21):
                chunk_matrix = train_df.iloc[:,
                                             :-2].loc[train_df['chunk'] == i].values
                instance_list.append(chunk_matrix)
                
                label_for_this_chunk = train_df[train_df['chunk'] == i].N.values[0]
                
                if label_for_this_chunk == 2:
                    print('equal 2, label_for_this_chunk is {}'.format(label_for_this_chunk))
                    instance_label.append(1)
                elif label_for_this_chunk == 3:
                    print('equal 3, label_for_this_chunk is {}'.format(label_for_this_chunk))
                    instance_label.append(2)
                elif label_for_this_chunk == 0:
                    print('equal 0, label_for_this_chunk is {}'.format(label_for_this_chunk))
                    instance_label.append(0)

    # each test csv file contain 6 chunks (chunks)
    elif phase == "test":
        test_df = pd.read_csv(path)
        #应该是在此处filter想要的column即可，取column时从.iloc[:,2:-2]---> [:,:-2]
        prefrontal_cols = [col for col in test_df if 'AF' in col] #JUNE11
        test_df = test_df[prefrontal_cols + ['N'] + ['chunk']] #JUNE11
        # test chunk id start from 21 to 26
        for i in range(21, 27):
            chunk_matrix = test_df.iloc[:,
                                        :-2].loc[test_df['chunk'] == i].values
            instance_list.append(chunk_matrix)
            
            label_for_this_chunk = test_df[test_df['chunk'] == i].N.values[0]
            if label_for_this_chunk == 2:
                print('equal 2, label_for_this_chunk is {}'.format(label_for_this_chunk))
                instance_label.append(1)
            elif label_for_this_chunk == 3:
                print('equal 3, label_for_this_chunk is {}'.format(label_for_this_chunk))
                instance_label.append(2)
            elif label_for_this_chunk == 0:
                print('equal 0, label_for_this_chunk is {}'.format(label_for_this_chunk))
                instance_label.append(0)

    instance_list = np.array(instance_list, dtype=np.float32) 
    instance_label = np.array(instance_label, dtype=np.int64)
    
    return instance_list, instance_label
    
    
    