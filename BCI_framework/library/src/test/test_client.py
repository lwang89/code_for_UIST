import pandas as pd
import socket, time
import pickle, threading


def send_chunk_to_trained_model(chunk_dataframe, port = 1243):

    #build socket
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.connect((socket.gethostname(), port))
    
    _socket.send(pickle.dumps(chunk_dataframe))

    #get response from server
    rec = _socket.recv(1024)
    rec_data = pickle.loads(rec)
    print(rec_data)
    _socket.close()

def test_sending():
    for i in range(0,15):
        time.sleep(1)
        data = [['tom', i], ['nick', i+1], ['juli', i+2]]
        data_df = pd.DataFrame(data, columns = ['Name', 'Age'])
        send_chunk_to_trained_model(data_df, 1243)

    print("cao ni da ye")

def threadFunc():
   for i in range(5):
       print('Hello from new Thread ')
       time.sleep(1)

if __name__ == '__main__':
    test_sending()

    ############ test code #############
    # th = threading.Thread(target=threadFunc)
    # th.start()
    # # Print some messages on console
    # for i in range(5):
    #     print('Hi from Main Thread')
    #     time.sleep(1)
    # # Wait for thread to finish
    # th.join()


        