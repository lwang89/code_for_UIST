import pandas as pd
import socket,time
import pickle
import threading

from data_analysis.run_model import predict_chunk_test_data

# This is designed for experiment.py
# Purpose: receive chunk test data
def receive_test_chunk_dataframe(isRunning,srvSocket,people_best_models,person_index,param_dict):
     
    print(not srvSocket._closed)
    
    while isRunning:
        try:
            # now our endpoint knows about the OTHER endpoint.
            clientsocket, address = srvSocket.accept()
            print(f"Connection from {address} has been established.")
            received_data_bytes = clientsocket.recv(1024)
            received_test_data_chunk = pickle.loads(received_data_bytes)
            print("server receive: ", type(received_test_data_chunk))
            print("server receive: ", received_test_data_chunk) 
            response_msg = "Server receive test data chunk sucessfully." + str(srvSocket._closed)
            msg = pickle.dumps(response_msg)
            clientsocket.send(msg)

            test_set = data_pre_process(received_test_data_chunk)
            predict_chunk_test_data(test_set, people_best_models, person_index, param_dict)

        except socket.timeout:
            print("We are here!!!!")
            isRunning = False
            continue
    print("ohhhhhhhhhh")

def run_server(predict_chunk_test_data, people_best_models, person_index, param_dict):
    try:
        port = 1243
        isRunning = True
        test_session_time = 10
        srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srvSocket.bind((socket.gethostname(), port))
        srvSocket.listen(5)
        srvSocket.settimeout(test_session_time)
    finally:
          pass 
    
    # receive_test_chunk_dataframe(isRunning, srvSocket)
    t1 = threading.Thread(target=receive_test_chunk_dataframe(isRunning,srvSocket,people_best_models,person_index,param_dict))
    t1.start()

def create_feature_index():
    MUSE_features_index = ["alpha_TP9", "alpha_AF7", "alpha_AF8", "alpha_TP10", "alpha_Left(TP9 + AF7)", "alpha_Right(TP9 + AF7)", "alpha_Front(AF7 + AF8)", "alpha_Back(TP9 + AF10)", "alpha_Average"]\
                + ["beta_TP9", "beta_AF7", "beta_AF8", "beta_TP10", "beta_Left(TP9 + AF7)", "beta_Right(TP9 + AF7)", "beta_Front(AF7 + AF8)", "beta_Back(TP9 + AF10)", "beta_Average"]\
                + ["delta_TP9", "delta_AF7", "delta_AF8", "delta_TP10", "delta_Left(TP9 + AF7)", "delta_Right(TP9 + AF7)", "delta_Front(AF7 + AF8)", "delta_Back(TP9 + AF10)", "delta_Average"]\
                + ["theta_TP9", "theta_AF7", "theta_AF8", "theta_TP10", "theta_Left(TP9 + AF7)", "theta_Right(TP9 + AF7)", "theta_Front(AF7 + AF8)", "theta_Back(TP9 + AF10)", "theta_Average"]\
                + ["gamma_TP9", "gamma_AF7", "gamma_AF8", "gamma_TP10", "gamma_Left(TP9 + AF7)", "gamma_Right(TP9 + AF7)", "gamma_Front(AF7 + AF8)", "gamma_Back(TP9 + AF10)", "gamma_Average"]
    return MUSE_features_index

def data_pre_process(received_test_data_chunk):
    return 0

if __name__ == '__main__':
    run_server()
