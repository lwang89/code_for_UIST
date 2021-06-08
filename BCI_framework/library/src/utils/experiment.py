import pandas as pd
from pandas import DataFrame
import socket
import json

# def train_model():
#     # When train session is done:
#     # 1. load train data csv file;
#     # 2. get trained model;
#     pass

# def predict_results():
#     # 1. start a server socket (use a seperate thread later) for a time length of test session
#     # 2. wait for test data chunks (Muse) sent from port, then predict;
#     # 3. close the server socket when time is out;
#     pass
def save_task_results(app, experiment_id, subject_id, results):
    """Store the result of the task performed by the subject

    1. Load data storage path for raw data from the config file: instance/config.py
    2. In the subject folder for raw data, create a file "{task_name}.csv" 
        to save the result of the task

    Args:
        app (Flask): The current flask app
        experiment_id (int): The ID for the current experiment
        subject_id (int): The ID for the current subject
        results (dict): The task result
    """
    print(results)

    path_dict = app.config.get("STORE_PATH")

    raw_data_path = path_dict["experiment_raw_data_path"] \
                    + "/exp_" + str(experiment_id) \
                    + "/sub_" + str(subject_id) \
                    + "/" + results["name"] + ".txt"

    with open(raw_data_path, 'w') as outfile:
        json.dump(results, outfile)


    # df = DataFrame(results["task_result"], index=[0])
    # print(df)
    # df.to_csv(raw_data_path, index=False, header=True)

    print("store task performance successfully")

def save_serial_feedback(app, experiment_id, subject_id, results):
    """Store the feedback for the current subject

    1. Load data storage path for post-experiment from the config file: instance/config.py
    2. In the subject folder for post-experiment, create a file "{questionnaire_name}.csv" 
        to save the subject feedback, questionnaire_name coule be:
            nasa_workload_index_train
            nasa_workload_index_test

    Args:
        app (Flask): The current flask app
        experiment_id (int): The ID for the current experiment
        subject_id (int): The ID for the current subject
        results (dict): The subject feedback collected in post-experiment
    """
    path_dict = app.config.get("STORE_PATH")
    sub_info_csv_path = path_dict["post_experiment_path"] \
                        + "/exp_" + str(experiment_id) \
                        + "/sub_" + str(subject_id) \
                        + "/" + results["name"] + ".csv"

    df = DataFrame(results, index=[0])
    print(df)
    df.to_csv(sub_info_csv_path, index=False, header=True)

    print("store subject feedback successfully")

def init_server_socket(port, test_session_time):
    try:

        srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srvSocket.bind((socket.gethostname(), port))
        srvSocket.listen(1000)
        srvSocket.settimeout(test_session_time)
        return srvSocket
    finally:
        pass


def load_model_train_params(app, experiment_id, subject_id):
    param_dict = app.config.get("MODEL_TRAINING_PARAMETERS").copy()

    # Set file path of traning and output
    path_dict = app.config.get("STORE_PATH")
    preprocessed_data_path = path_dict["experiment_preprocessed_data_path"] \
                    + "/exp_" + str(experiment_id) \
                    + "/sub_" + str(subject_id)
    analyzed_data_path = path_dict["experiment_analyzed_data_path"] \
                    + "/exp_" + str(experiment_id) \
                    + "/sub_" + str(subject_id)
    param_dict["result_save_dir"] = analyzed_data_path
    param_dict["train_dir"] = preprocessed_data_path

    device = param_dict["device"]

    # Set train file names
    slide_window_size = param_dict["slide_window_size"]
    slide_interval = param_dict["slide_interval"]
    train_file_name = device + '_train_task_{}_{}.csv'.format(slide_window_size, slide_interval)
    param_dict["train_files"] = [train_file_name]
    
    # Set feature index and col index
    device_feature_index = app.config.get("FEATURE_INDEX").copy()
    col_index = app.config.get("COL_INDEX").copy()

    feature_index = device_feature_index[device]
    col_index = feature_index + col_index

    param_dict["feature_index"] = feature_index
    param_dict["col_index"] = col_index

    # Set input size
    param_dict["input_size"] = len(feature_index)
    return param_dict


def load_model_test_params(app):
    param_dict = app.config.get("PREDICTION_SERVER_PARAMETERS").copy()

    device = param_dict["device"]
    
    # Set feature index and col index
    device_feature_index = app.config.get("FEATURE_INDEX").copy()
    feature_index = device_feature_index[device]
    param_dict["feature_index"] = feature_index

    return param_dict