import pandas as pd
import socket,time
import pickle
import threading
import numpy as np

from .run_model import predict_chunk_test_data
from .brain_data import personal_test_brain_data

# This is designed for experiment.py
# Purpose: receive chunk test data
def receive_test_chunk_dataframe(isRunning, srvSocket, people_best_models, prediction_params):

    print(not srvSocket._closed)
    
    while isRunning:
        try:
            # now our endpoint knows about the OTHER endpoint.
            # print("server running loop")
            clientsocket, address = srvSocket.accept()
            # print(f"Connection from {address} has been established.")
            received_data_bytes = clientsocket.recv(10240)

            # print("receive data successs")
            # print("received_data_bytes")
            received_test_data_chunk = pickle.loads(received_data_bytes)
            # print("server receive: ", type(received_test_data_chunk))
            # print("server receive: ", received_test_data_chunk) 


            # response_msg = "Server receive test data chunk sucessfully." + str(srvSocket._closed)
            # msg = pickle.dumps(response_msg)
            # clientsocket.send(msg)

            if received_test_data_chunk.shape[0]==prediction_params["slide_window_size"]:
                # print("server receive: ", received_test_data_chunk.shape) 
                # print("Predict :")

                chunk_test_np_array = data_pre_process(received_test_data_chunk, prediction_params["feature_index"])
                test_set = personal_test_brain_data(chunk_test_np_array)

                predicted_label = predict_chunk_test_data(test_set, people_best_models, prediction_params)
                print("Predicted label :{}".format(predicted_label))

        except socket.timeout:
            print("We are here!!!!")
            isRunning = False
            continue


def data_pre_process(data_chunk_df, feature_index):
    data_chunk_features_df = data_chunk_df.loc[:, feature_index]
    data_chunk_np_array_2d = data_chunk_features_df.to_numpy()
    data_chunk_np_array_3d = np.array([data_chunk_np_array_2d], dtype=np.float32)

    test_set = personal_test_brain_data(data_chunk_np_array_3d)
    return test_set