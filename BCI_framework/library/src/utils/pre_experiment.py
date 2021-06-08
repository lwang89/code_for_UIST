import os
from pandas import DataFrame
import pandas as pd
import json

def initialize_subjcet_id(app, experiment_id):
    """Initialize ID for the current subject

    1. Scan the first path for the current experiment id:
        First path is set by the config file : instance/config.py
        Path example: "pre_experiment_path": "library/storage/pre_experiment"
    2. Go through all the subject folders, find the largest 
       subject id, say X, return X+1

    Args:
        app (Flask): The current flask app
        experiment_id (int): The current experiment ID
    
    Returns:
        int: The number labeled for the current subject.
        It should be one plus the largest subject ID under the current experiment

    """
    path_dict = app.config.get("STORE_PATH")

    # We could use anyone of those 7 places to scan existing subjects
    pre_exp_folder_path = path_dict["pre_experiment_path"] \
                        + "/exp_" + str(experiment_id)
    subject_dirs = os.listdir(pre_exp_folder_path)
    subject_id_list = []

    for subject in subject_dirs:
        subject_id_list.append(int(subject[4:]))
    
    if len(subject_id_list):
        subject_id = max(subject_id_list) + 1
    else:
        subject_id = 0

    return subject_id


def update_subject_list(app, experiment_id, subject_id):
    """Add the current subject state to the subject list of the current experiment
    
    1. Load the subject list json file under the current experiment
    2. Add the status information for the current subject
    3. Write back to the json file

    Args:
        app (Flask): The current flask app
        experiment_id (int): The ID for the current experiment
        subject_id (int): The ID for the current subject
    """
    path_dict = app.config.get("STORE_PATH")
    subject_list_file_path = path_dict["log_path"] \
                            + "/exp_" + str(experiment_id) \
                            + "/subject_list.json"

    # load json file to dict variable
    with open(subject_list_file_path, 'r') as load_f:
        subject_list = json.load(load_f)

    # add current subject information to dict
    subject_list.append({"subject_id": subject_id, "status": "created"})

    # write dict variable back to json file
    with open(subject_list_file_path, "w") as dump_f:
        json.dump(subject_list, dump_f)

    print("\n****************************************************")
    print("Add subject id " + str(subject_id) \
            + " for experiment " + str(experiment_id))
    print("update subject list successfully")
    print("****************************************************")


def initialize_subjcet_folders(app, experiment_id, subject_id):
    """Initialize folders for the current subject of the current experiment

    1. Load data storage paths from the config file: instance/config.py
    2. For all storage paths, create a folder for current subject
       under current experiment with name exp_{id}/sub_{id} if not exists.

    Args:
        app (Flask): The current flask app
        experiment_id (int): The ID for the current experiment
        subject_id (int): The ID for the current subject
    """
    print("\n****************************************************")
    print("initialize subject folders")

    path_dict = app.config.get("STORE_PATH")

    for path_key in path_dict:
        path_value = path_dict[path_key] \
                    + "/exp_" + str(experiment_id) \
                    + "/sub_" + str(subject_id)
        
        if not os.path.exists(path_value):
            os.makedirs(path_value)
            print("create ---- " + path_value)
        else:
            print("already exists ---- " + path_value)
    
    print("initialize subject folders successfully")
    print("****************************************************")


def store_subject_information(app, experiment_id, subject_id, results):
    """Store the information for the current subject

    1. Load data storage path for pre-experiment from the config file: instance/config.py
    2. In the subject folder for pre-experiment, create a file "info.csv" to save the subject information

    Args:
        app (Flask): The current flask app
        experiment_id (int): The ID for the current experiment
        subject_id (int): The ID for the current subject
        results (dict): The subject information collected in pre-experiment
    """
    path_dict = app.config.get("STORE_PATH")
    sub_info_csv_path = path_dict["pre_experiment_path"] \
                        + "/exp_" + str(experiment_id) \
                        + "/sub_" + str(subject_id) \
                        + "/info.csv"
    
    # Turn any list into strings
    new_results = dict()
    for item_key in results:
        if type(results[item_key]) == list:
            new_results[item_key] = ','.join(results[item_key])
        else:
            new_results[item_key] = results[item_key]

    df = DataFrame(new_results, index=[0])
    print(df)

    df.to_csv(sub_info_csv_path, index=False, header=True)

    print("store subject information successfully")
    print("****************************************************")