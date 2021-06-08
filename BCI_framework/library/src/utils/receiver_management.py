from library.src.data_receiver.Muse.osc_server_mindmonitor import muse_receiver
from library.src.data_receiver.fnirs.fnirs_receiver import fnirs_receiver
from library.src.data_receiver.gsr.gsr_receiver import gsr_receiver

import os

BOOSTED_DEVICES = []
RECEIVERS = dict()


def init_boosted_devices(boosted_devices):
    global BOOSTED_DEVICES

    BOOSTED_DEVICES = boosted_devices


def init_receivers(app, experiment_id, subject_id):
    """Initialize receivers that are in BOOSTED_DEVICES

    1. Generate the file paths to store the streaming data: 
       muse: exp_{experiment id}/sub_{subject id}/muse.csv
    2. Load data record parameters (address, port, raw_data_path, .etc) 
       from the config file: instance/config.py
    3. Instanciate objects for selected receivers

    Args:
        app (Flask): The current flask app
        experiment_id (int): The ID for the current experiment
        subject_id (int): The ID for the current subject
    """
    global BOOSTED_DEVICES, RECEIVERS


    # Make the path for data storage of the current subject
    path_dict = app.config.get("STORE_PATH")

    raw_data_path = path_dict["experiment_raw_data_path"] \
                    + "/exp_" + str(experiment_id) \
                    + "/sub_" + str(subject_id)
                    # + "/muse.csv"
    slide_window_data_path = path_dict["experiment_slide_window_data_path"] \
                    + "/exp_" + str(experiment_id) \
                    + "/sub_" + str(subject_id)
    preprocessed_data_path = path_dict["experiment_preprocessed_data_path"] \
                    + "/exp_" + str(experiment_id) \
                    + "/sub_" + str(subject_id)

    slide_window_parameters = app.config.get("RAW_DATA_SLIDE_WINDOW_PARAMETERS")
    data_receiver_parameters = app.config.get("DATA_RECEIVER_PARAMETERS")

    for boosted_device in BOOSTED_DEVICES:          # loop over all devices to boost
        for device_params in data_receiver_parameters:     # loop over all devices available
            if device_params["name"] == boosted_device:

                if boosted_device == "muse":
                    muse_receiver = init_muse_receiver(device_params, raw_data_path, slide_window_data_path, preprocessed_data_path, slide_window_parameters)
                    RECEIVERS[boosted_device] = muse_receiver
                    print("muse receiver initialized!")
                
                elif boosted_device == "fnirs":
                    fnirs_receiver = init_fnirs_receiver(device_params, raw_data_path, preprocessed_data_path, slide_window_parameters)
                    RECEIVERS[boosted_device] = fnirs_receiver
                    print("fnirs receiver initialized!")
                    pass

                elif boosted_device == "gsr":
                    if not os.path.exists(raw_data_path + '/empatica_gsr'):
                        os.makedirs(raw_data_path + '/empatica_gsr')
                    gsr_receiver = init_gsr_receiver(device_params, raw_data_path + '/empatica_gsr')
                    RECEIVERS[boosted_device] = gsr_receiver
                    print("gsr receiver initialized!")


def calibration_start():
    """Call receivers in need to start calibration
    """
    global BOOSTED_DEVICES, RECEIVERS
    for receiver_name in BOOSTED_DEVICES:
        RECEIVERS[receiver_name].calibration_start()


def calibration_end():
    """Call receivers in need to stop calibration
    """
    for receiver_name in BOOSTED_DEVICES:
        RECEIVERS[receiver_name].calibration_end()


def start_session(session_type):
    """Call receivers to start a new session

    The receivers should reset the internal cache and update
    their internal variable for session_type.

    Args:
        session_type (string): "train"/"test"
    """
    global BOOSTED_DEVICES, RECEIVERS
    for receiver_name in BOOSTED_DEVICES:
        RECEIVERS[receiver_name].start_session(session_type)


def update_label(label=None, serial_type=None):
    """Let receivers update the label.
    
    The new label should be the default label should the input be None.

    Args:
        label (int, optional): Label for the data. Defaults to None.
    """
    global BOOSTED_DEVICES, RECEIVERS
    for receiver_name in BOOSTED_DEVICES:
        RECEIVERS[receiver_name].update_label(label=label, serial_type=serial_type)


def save_data_to_CSVs():
    """Let receivers save data to local CSV files

    The data would include raw data, preprocessed data.
    """
    global BOOSTED_DEVICES, RECEIVERS
    print("********************************")
    for receiver_name in BOOSTED_DEVICES:
        RECEIVERS[receiver_name].save_data_to_CSVs()
    print("********************************")


def stop():
    """Let receivers stop listening and recording.
    """
    global BOOSTED_DEVICES, RECEIVERS
    for receiver_name in BOOSTED_DEVICES:
        RECEIVERS[receiver_name].stop()


################### Internal Functions ###################

def init_muse_receiver(muse_parameters, raw_data_path, slide_window_data_path, preprocessed_data_path, slide_window_parameters):
    """Initialize Muse receiver, let it listen to a specific port and save data locally


    1. Initialize the Muse receiver instance with the parameters loaded
    2. Let the receiver listen to the port, generate raw data DataFrame
        and slide window DataFrame in real time. Save raw data in local
        csv file under the path set by config file.
    3. Local file example: library/storage/experiment/raw_data/exp_0/
        sub_0/muse.csv

    Args:
        muse_parameters (dict): The parameters for muse receiver
        raw_data_path (str): The path to save raw data
        slide_window_data_path (str): The path to save slide window data
    """
    # load parameters from config.py
    # Set up data receive ip address and port

    # Load params to initialize Muse receiver

    preprocessing_flag = muse_parameters["preprocessing_flag"]
    preprocessing_API = muse_parameters["preprocessing_API"]
    default_label = muse_parameters["default_label"]
    send_port = muse_parameters["send_port"]
    
    # Initialize Muse receiver
    mr = muse_receiver(raw_data_path, slide_window_data_path, slide_window_parameters,
                        preprocessed_data_path, preprocessing_flag,
                        preprocessing_API, default_label, send_port)

    # Params to listen to the port
    listen_ip_address = muse_parameters["listen_ip_address"]
    listen_port = muse_parameters["listen_port"]

    # Let the receiver listen to the port
    mr.listen(listen_ip_address, listen_port)
    print("initialize muse receiver successfully")
    return mr


def init_fnirs_receiver(fnirs_parameters, raw_data_path, preprocessed_data_path, slide_window_parameters):
    default_label = fnirs_parameters["default_label"]
    send_port = fnirs_parameters["send_port"]

    fr = fnirs_receiver(raw_data_path, preprocessed_data_path, slide_window_parameters, default_label, send_port)

    fr.listen()
    return fr

def init_gsr_receiver(gsr_params, raw_data_path):
    default_label = gsr_params["default_label"]
    listen_ip_address = gsr_params["listen_ip_address"]
    listen_port = gsr_params["listen_port"]
    device_id = gsr_params["device_id"]

    gr = gsr_receiver(raw_data_path, default_label, listen_ip_address, listen_port, device_id)

    gr.listen()

    return gr