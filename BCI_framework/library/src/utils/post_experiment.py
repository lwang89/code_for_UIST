from pandas import DataFrame
import pandas as pd

def store_subject_feedback(app, experiment_id, subject_id, results):
    """Store the feedback for the current subject

    1. Load data storage path for post-experiment from the config file: instance/config.py
    2. In the subject folder for post-experiment, 
       create a file "{questionnaire_name}.csv" to save the subject feedback, 
       questionnaire_name coule be:
       
       questionnaire_1
       questionnaire_2
       nasa_workload_index_train
       nasa_workload_index_test

    Args:
        app (Flask): The current flask app
        experiment_id (int): The ID for the current experiment
        subject_id (int): The ID for the current subject
        results (dict): The subject feedback collected in post-experiment
    """
    path_dict = app.config.get("STORE_PATH")
    sub_info_csv_path = path_dict["post_experiment_path"] + "/exp_" + str(experiment_id) + "/sub_" + str(subject_id) + "/" + results["name"] + ".csv"

    df = DataFrame(results, index=[0])
    print(df)

    df.to_csv(sub_info_csv_path, index=False, header=True)

    print("store subject feedback successfully")