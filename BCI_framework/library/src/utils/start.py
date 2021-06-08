import os
import json


def load_experiment_parameter(app):
    """ Show experiment parameters and collect ID from console.

    1. Load parameters for all experiments from the config file
       Config file path: instance/config.py
    2. Show the parameters in the back end console, 
       let the operator input the experiment ID
    3. Return the experiment ID and the corresponding parameters

    Args:
        app: (Flask) The current flask app
    
    Returns:
        tuple(int, dict): The first int value is the experiment ID 
            collected from the console. The second dictionary is
            the parameters for this experiment.

    """

    # list all experiment parameters
    exp_list = app.config.get("EXPERIMENT_PARAMETERS")
    
    print("\n****************************************************")
    print("Please select the experiment you want to perform: \n")

    # Show experiment parameters
    for exp_params in exp_list:
        print("\n****************************************************")
        for key in exp_params:
            if (key != "sessionParameters"):
                print(key, "\t : ", exp_params[key])

    # Receive the input from command line
    exp_id = int(input("\nPlease input experiment ID: "))

    for exp_params in exp_list:
        if exp_params["experimentID"] == exp_id:
            print("load experiment parameters successfully")
            return (exp_id, exp_params)

    # print alert if we can not find the experiment ID that operator inputed
    print("No such experiment with ID: ", exp_id)


def initialize_experiment_folders(app, experiment_id):
    """ Initialize folders to save data for the current experiment

    1. Load data storage paths from the config file: instance/config.py
    2. For all storage paths, create a folder for current experiment 
       with name exp_{id} if not exists.

    Args:
        app (Flask): The current flask app
        experiment_id (int): The ID for the current experiment

    """
    print("\n****************************************************")
    # 1. create if the folder exp_"exp+id" does not exist;
    path_dict = app.config.get("STORE_PATH")

    for path_key in path_dict:
        path_value = path_dict[path_key] + "/exp_" + str(experiment_id)
        if not os.path.exists(path_value):
            os.makedirs(path_value)
            print("create ---- " + path_value)
        else:
            print("already exists ---- " + path_value)
    

    print("Initialize experiment folders successfully!")
    print("****************************************************")
    

def initialize_subject_list(app, experiment_id):
    """ Initialize subject list for the current experiment under 

    1. Check whether subject_list.json exists at log path 
       (set by the config file : instance/config.py),
       if so, print infomation, if not, create a new file.
    2. subject list path example: library/src/storage/log/exp_0
    
    Log path example: "log_path" : "library/storage/log"

    Args:
        app (Flask): The current flask app
        experiment_id (int): The ID for the current experiment

    """
    path_dict = app.config.get("STORE_PATH")
    subject_list_file_path = path_dict["log_path"] \
                            + "/exp_" + str(experiment_id) \
                            + "/subject_list.json"

    print("\n****************************************************")
    print("Initialize subject list")
    
    if os.path.exists(subject_list_file_path):
        print("already exists ---- " + subject_list_file_path)
    else:
        # write dict variable back to json file
        with open(subject_list_file_path, "w") as dump_f:
            json.dump([], dump_f)
        print("create ---- " + subject_list_file_path)
    
    print("Initialize subject list successfully")
    print("Now you can start the experiment!")
    print("****************************************************")