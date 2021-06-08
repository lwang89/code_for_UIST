from flask import Flask, request, render_template, redirect, url_for, abort
from jinja2 import TemplateNotFound
import json
import threading

from library.src.utils import start as st
from library.src.utils import pre_experiment as pre
from library.src.utils import experiment as exp
from library.src.utils import post_experiment as post
from library.src.utils import receiver_management

from library.src.data_analysis import run_model
from library.src.data_analysis.prediction_server import receive_test_chunk_dataframe

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# basic info
SUBJECT_ID = 0
EXPERIMENT_ID = 0

PREDICTION_SERVER_THREAD = None

############################################################################
# Start
@app.route('/', methods=['GET'])
def hello_world():
    if request.method == 'GET':

        try:
            return render_template('vue/index.html')
        except TemplateNotFound:
            abort(404)


@app.route('/get_experiment_parameters', methods=['GET'])
def get_experiment_parameters():
    global EXPERIMENT_ID
 
    EXPERIMENT_ID, cur_experiment_parameters = st.load_experiment_parameter(app)
    receiver_management.init_boosted_devices(cur_experiment_parameters["boosted_devices"])
    st.initialize_experiment_folders(app, EXPERIMENT_ID)
    st.initialize_subject_list(app, EXPERIMENT_ID)

    return json.dumps(cur_experiment_parameters)


############################################################################
# Pre-experiment
@app.route('/get_subject_id', methods=['GET'])
def get_subject_id():
    global EXPERIMENT_ID, SUBJECT_ID
    SUBJECT_ID = pre.initialize_subjcet_id(app, EXPERIMENT_ID)
    print("subject ID = ", SUBJECT_ID)

    return str(SUBJECT_ID)


@app.route('/save_pre_experiment_result', methods=['POST'])
def save_pre_experiment_result():
    global EXPERIMENT_ID, SUBJECT_ID
    results = json.loads(request.data)
    print("receive pre experiment subject information")
    print(results)

    pre.update_subject_list(app, EXPERIMENT_ID, SUBJECT_ID)
    pre.initialize_subjcet_folders(app, EXPERIMENT_ID, SUBJECT_ID)
    pre.store_subject_information(app, EXPERIMENT_ID, SUBJECT_ID, results)

    receiver_management.init_receivers(app, EXPERIMENT_ID, SUBJECT_ID)

    return "Save pre-experiment result successfully"

@app.route('/post_device_ready', methods=['POST'])
def post_device_ready():

    print("\n****************************************************")
    response = str(input("\nPlease input anything when the device is ready: \n"))
    print("****************************************************\n")

    return response

@app.route('/start_rest_before_experiment', methods=['POST'])
def start_rest_before_experiment():
    print("\n****************************************************")
    print("Rest before experiment start!")

    receiver_management.calibration_start()
    print("****************************************************\n")

    return "Start rest before experiment successfully"


@app.route('/end_rest_before_experiment', methods=['POST'])
def end_rest_before_experiment():
    print("\n****************************************************")
    print("Rest before experiment start!")

    receiver_management.calibration_end()
    print("****************************************************\n")

    return "End rest before experiment successfully"


############################################################################
# Experiment
@app.route('/start_session', methods=['POST'])
def start_session():
    """Set the session type for saving data, re-initialize all DataFrame
    """
    print("\n****************************************************")
    print("Session start!")
    # The results here is Session info:
    # results["sessionType"], results["sessionID"], results["sessionType"]
    results = json.loads(request.data)
    print(results)

    session_type = results["sessionType"]
    receiver_management.start_session(session_type)
    print("****************************************************\n")

    return "Start session successfully"


@app.route('/start_task', methods=['POST'])
def start_task():
    print("\n****************************************************")
    print("Task start!")

    # The results here is Serial info:
    # results["experimentID"], results["sessionID"]
    # results["serialID"], results["bigN"]
    results = json.loads(request.data)
    print(results)

    # Set the label for received data from default to bigN
    receiver_management.update_label(label=results["bigN"], serial_type="task")
    print("****************************************************\n")

    return "Start task successfully"


@app.route('/end_task', methods=['POST'])
def end_task():
    print("\n****************************************************")
    print("Task end!")

    # The results here is result of the task performed by the subject:
    # results["task_result"], results["name"], results["serial_info"]
    results = json.loads(request.data)

    exp.save_task_results(app, EXPERIMENT_ID, SUBJECT_ID, results)

    # Set the label for received data to default
    receiver_management.update_label(label=None, serial_type="task")
    print("****************************************************\n")

    return "End task successfully"

@app.route('/start_rest', methods=['POST'])
def start_rest():
    print("\n****************************************************")
    print("Rest start!")

    # The results here is Serial info:
    # results["experimentID"], results["sessionID"]
    # results["serialID"], results["bigN"]
    results = json.loads(request.data)

    # Set the label for received data from default to bigN
    receiver_management.update_label(label=results["bigN"], serial_type="rest")
    print("****************************************************\n")

    return "Start rest successfully"


@app.route('/end_rest', methods=['POST'])
def end_rest():
    print("\n****************************************************")
    print("Rest end!")

    # Set the label for received data to default
    receiver_management.update_label(label=None, serial_type="rest")
    print("****************************************************\n")

    return "End rest successfully"

@app.route('/save_serial_feedback', methods=['POST'])
def save_serial_feedback():
    global EXPERIMENT_ID, SUBJECT_ID
    print("\n****************************************************")
    print("Save serial feedback")
    results = json.loads(request.data)
    # print(results)
    exp.save_serial_feedback(app, EXPERIMENT_ID, SUBJECT_ID, results)
    print("****************************************************\n")

    return "Save post-experiment results successfully"

@app.route('/end_session', methods=['POST'])
def end_session():
    """Save data to csv
    """
    global EXPERIMENT_ID, SUBJECT_ID, PREDICTION_SERVER_THREAD
    print("\n****************************************************")
    print("Session end!")
    # The results here is Session info:
    # results["sessionType"], results["sessionID"], results["sessionType"]
    results = json.loads(request.data)
    print(results)

    receiver_management.save_data_to_CSVs()

    # use "if False" to go into develop mode: 
    if results["sessionType"] == "train":
    # if False:
        print("Train session end!")

        #start loading parameters and then training model
        train_param_dict = exp.load_model_train_params(app, EXPERIMENT_ID, SUBJECT_ID)

        people_best_models = run_model.run(train_param_dict)

        print("-------------------------------------------\n\n\n")
        print("Model Training  Done !!!!!!!!!!!!!!!!!!!!")
        print("\n\n\n-------------------------------------------")

        # use flag isRunning to start server socket, and wrap in in args
        isRunning = True

        prediction_param_dict = exp.load_model_test_params(app)
        srvSocket = exp.init_server_socket(prediction_param_dict["port"],
                                        prediction_param_dict["test_session_time"])
        args = [isRunning, srvSocket, people_best_models, prediction_param_dict]

        PREDICTION_SERVER_THREAD = threading.Thread(
                                            target=receive_test_chunk_dataframe,
                                            args=args)
        PREDICTION_SERVER_THREAD.start()

        print("-------------------------------------------\n\n\n")
        print("Prediction Server Start !!!!!!!!!!!!!!!!!!!!")
        print("\n\n\n-------------------------------------------")
    
    print("****************************************************\n")

    return "End session successfully"


@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    """Stop the OSC server

    1. Call the stop function on global variable MUSE_RECEIVER
        to stop recording data
    2. Reset the MUSE_RECEIVER as None
    """
    print("\n****************************************************")
    print("Stop recording")
    receiver_management.stop()
    print("****************************************************\n")

    return "Stop recording successfully"


############################################################################
# Post-experiment
@app.route('/save_post_experiment_results', methods=['POST'])
def save_post_experiment_results():
    global EXPERIMENT_ID, SUBJECT_ID
    print("receive post experiment feedback")
    results = json.loads(request.data)
    # print(results)
    post.store_subject_feedback(app, EXPERIMENT_ID, SUBJECT_ID, results)

    return "Save post-experiment results successfully"
