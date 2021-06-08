from threading import Lock, Thread
import serial
import numpy as np
import pandas as pd
from operator import methodcaller
import time
from pathlib import Path
import socket
import pickle
from scipy.io import savemat

from library.src.utils.generating_slide_windows import generate_slide_window_chunks
from library.src.data_preprocessing.fnirs import fnirs

class fnirs_receiver:
    def __init__(self, raw_data_path, preprocessed_data_path, slide_window_params,
                default_label, send_port):
        # Receiver settings from parameters
        self.raw_data_path = str(Path(__file__).parent / ("../../../../" + raw_data_path))
        self.preprocessed_data_path = preprocessed_data_path
        self.slide_window_params = slide_window_params
        self.default_label = default_label
        self.send_port = send_port

        # Internal variables
        # self.label = default_label
        self.label = default_label
        self.session_type = "train"         # (string) The initial session type
        self.serial_type = "task"           # (string) The flag for current state inside a serial ("task"/"rest")
        self.column_index = []              # (list) List of column names.
                                            # It will be initialized by init_column_index() and used by init_raw_df()
        self.slide_window_column_index = []

        self.column_index_A_I = []
        self.column_index_A_phi = []
        self.column_index_B_I = []
        self.column_index_B_phi = []
        self.column_index_AB = []           # (list) List of column names for AB channels.
                                            # It will be initialized by init_column_index()
        self.column_index_C_I = []
        self.column_index_C_phi = []
        self.column_index_D_I = []
        self.column_index_D_phi = []
        self.column_index_CD = []           # (list) List of column names for CD channels. 
                                            # It will be initialized by init_column_index()

        self.column_index_ABCD_T = []       # (list) List of column names for channels of ABCD and T.
                                            # It will be initialized by init_column_index()
        self.row_index = 0                  # (int) Index of each row
        self.chunk_index_dict = dict()      # (list) List of index of chunk of each slide window setting

        self.raw_df = None                  # (Pandas DataFrame) Container of all raw data. 
                                            # It should be updated on real time.
        self.preprocessed_slide_window_df_dict = dict()         # (list(Pandas DataFrame)) Container of the current
                                                                # slide window, maintained by update_slide_window_df_list()
        self.preprocessed_chunk_df_dict = dict()                # (dict(setting_index: Dataframe))
                                                                # Container of the new generate chunks by the new row of data,
                                                                # cache for sending to prediction server

        self.calibration_start_row = 0      # (int) The starting row for ssy0 initialization
        self.calibration_end_row = 0        # (int) The ending row for ssy0 initialization

        self.ssy0_AB = set()                # (set(mlarray.double, mlarray.double))
                                            # Container of the initialized ssy0 for AB channels
        self.ssy0_CD = set()                # (set(mlarray.double, mlarray.double))
                                            # Container of the initialized ssy0 for CD channels

        self.ser = serial.Serial(port='/dev/ttyUSB0',
                                 baudrate=115000, #115200
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.EIGHTBITS)
        self.lock = Lock()
        self.STOP_FLAG = False
        self.brain_thread = Thread(target=self.brainLoop, args=[])

        # Initialize internal variables and local file
        self.init_column_index()
        self.init_all_df()
        self.init_chunk_index()
        self.connect_matlab_engine()


    def init_column_index(self):
        """Initialize list of column names
        """
        self.column_index_A_I = ['AC-A1', 'AC-A2', 'AC-A21', 'AC-A22']
        self.column_index_A_phi = ['PH-A1', 'PH-A2', 'PH-A21', 'PH-A22']
        self.column_index_B_I = ['AC-B1', 'AC-B2', 'AC-B21', 'AC-B22']
        self.column_index_B_phi = ['PH-B1', 'PH-B2', 'PH-B21', 'PH-B22']

        self.column_index_AB = self.column_index_A_I + self.column_index_A_phi\
                            + self.column_index_B_I + self.column_index_B_phi

        self.column_index_C_I = ['AC-C3', 'AC-C4', 'AC-C23', 'AC-C24']
        self.column_index_C_phi = ['PH-C3', 'PH-C4', 'PH-C23', 'PH-C24']
        self.column_index_D_I = ['AC-D3', 'AC-D4', 'AC-D23', 'AC-D24']
        self.column_index_D_phi = ['PH-D3', 'PH-D4', 'PH-D23', 'PH-D24']

        self.column_index_CD = self.column_index_C_I + self.column_index_C_phi\
                            + self.column_index_D_I + self.column_index_D_phi

        self.column_index_ABCD_T =  ['T']\
                                + self.column_index_AB\
                                + self.column_index_CD

        self.column_index = ['row_index', 'timestamp', 'label']\
                            + self.column_index_ABCD_T

        self.slide_window_column_index = ['label', 'chunk', 'row_index', 'timestamp',\
                                        'dO_I_AB', 'dD_I_AB', 'dO_phi_AB', 'dD_phi_AB',\
                                        'dO_I_CD', 'dD_I_CD', 'dO_phi_CD', 'dD_phi_CD']


    def init_all_df(self):
        """Initialize raw_df and the list of slide windows of all settings
        """
        # initialize raw DataFrame ['row_index', 'timestamp', 'label', 'T', ABCD]
        self.raw_df = pd.DataFrame(columns=self.column_index)

        # initialize slide window dataframes
        self.preprocessed_slide_window_df_dict = dict()

        # initialize slide window DFs dict for task periods
        # ['label', 'chunk', 'row_index', 'timestamp', ABCD_I_phi]
        preprocessed_slide_window_df_task = dict()
        for index in list(range(len(self.slide_window_params))):
            new_chunk_df = pd.DataFrame(columns=self.slide_window_column_index)
            preprocessed_slide_window_df_task[index] = new_chunk_df
        self.preprocessed_slide_window_df_dict["task"] = preprocessed_slide_window_df_task

        # initialize slide window dfs dict for rest periods
        # ['label', 'chunk', 'row_index', 'timestamp', ABCD_I_phi]
        preprocessed_slide_window_df_rest = dict()
        for index in list(range(len(self.slide_window_params))):
            new_chunk_df = pd.DataFrame(columns=self.slide_window_column_index)
            preprocessed_slide_window_df_rest[index] = new_chunk_df
        self.preprocessed_slide_window_df_dict["rest"] = preprocessed_slide_window_df_rest


    def init_chunk_index(self):
        # initialize chunk index for slide windows
        self.chunk_index_dict = dict()
        self.chunk_index_dict["task"] = dict()
        self.chunk_index_dict["rest"] = dict()
        for index in list(range(len(self.slide_window_params))):
            self.chunk_index_dict["task"][index] = 0
            self.chunk_index_dict["rest"][index] = 0


    def connect_matlab_engine(self):
        print("\nTry to connect matlab engine\n")
        # Start the connection to matlab engine
        fnirs.init_matlab_engine()
        print("\nMATLAB engine connected \n")


    def brainLoop(self):
        """ The main loop inside the thread to receive data from the fnirs device.
        """
        while not self.STOP_FLAG:                       
            if self.STOP_FLAG: return
            else:
                try:                   
                    byte_packet = self.ser.read_until()
                    is_valid, new_row_df = self.parse(byte_packet)
                    if is_valid:

                        # Filter out necessary features
                        new_row_df = new_row_df.loc[:, self.column_index_ABCD_T]

                        # Add features
                        new_row_df = self.add_features(new_row_df)

                        # Add new row to raw_df
                        self.raw_df = pd.concat([self.raw_df, new_row_df])

                        # Reset index for raw df
                        self.raw_df = self.raw_df.reset_index(drop=True)

                        self.update_slide_window_df_list()

                        # Send the chunk for test session through socket
                        if self.session_type == "test":
                            self.send_chunks_to_prediction()

                except:
                    print("\n\n\n\nmalformed packet")
                    # print(byte_packet)
                    print("\n\n\n\n")

    def parse(self, byte_packet):
        is_valid = True
        packet_list = byte_packet.decode('utf-8').strip().split()
        packet_list = list(map(methodcaller("split","="), packet_list))

        # If the length is incorrect, return (False, None)
        if (packet_list == None or len(packet_list) != 49):
            is_valid = False
            return (is_valid, None)
        
        packet_dict = {x[0]: np.float64(x[1]) for x in packet_list}

        # Make the values in the dictionary wrapped in a list
        # Example:
        #   Before wrapping: {"key": "value"}
        #   After wrapping: {"key": ["value"]}
        for key in packet_dict:
            # print("{} : {}".format(key, packet_dict[key]))
            packet_dict[key] = [packet_dict[key]]

        df = pd.DataFrame.from_dict(packet_dict)
        return (is_valid, df)

    def add_features(self, row_df):
        # Add the following columns:
        #   ["row_index", "timestamp", "label"]

        # Add row_index
        row_df['row_index'] = [self.row_index]
        self.row_index = self.row_index + 1

        # Add timestamp
        timestamp = int(round(time.time() * 1000))
        row_df['timestamp'] = [timestamp]

        # Add label
        row_df['label'] = [self.label]

        return row_df
    
    def update_slide_window_df_list(self):
        # Empty the cache dict for new slide window chunks
        self.preprocessed_chunk_df_dict = dict()

        # Generate the chunks for when a current new row is added
        # Generate the new indices for the slide window settings
        # Generate the slide window DFs with new chunks attached to the end

        temp_chunk_df_dict = generate_slide_window_chunks(self.raw_df,
                                                            self.slide_window_params, 
                                                            self.default_label,
                                                            self.chunk_index_dict[self.serial_type])
        # columns now:
        #   ['chunk', 'row_index', 'timestamp', 'label', 'T', ABCD]

        # print("chunks:")
        # print(temp_chunk_df_dict)

        # Update chunk index and slide window DF for new chunks of each setting
        for index in temp_chunk_df_dict:
            chunk_df = temp_chunk_df_dict[index]
            # columns now:
            #   ['chunk', 'row_index', 'timestamp', 'label', 'T', ABCD]

            channel_dict = self.chunk_df_to_dict(chunk_df)
            # columns lost here:
            #   ['chunk', 'row_index', 'timestamp', 'label']
            # keys now:
            #   ['A_I', 'A_phi', 'B_I', 'B_phi', 'C_I', 'C_phi', 'D_I', 'D_phi', 'T']

            matlab_channel_dict = self.dict_to_matlab_dict(channel_dict)
            # keys now:
            #   ['A_I', 'A_phi', 'B_I', 'B_phi', 'C_I', 'C_phi', 'D_I', 'D_phi', 'T']

            # Call matlab function to do preprocessing, using the existing ssy0 data
            # For AB channels
            dO_I_AB, dD_I_AB, dO_phi_AB, dD_phi_AB = fnirs.preprocess(self.ssy0_AB[0],
                                                            self.ssy0_AB[1],
                                                            matlab_channel_dict['A_I'],
                                                            matlab_channel_dict['A_phi'],
                                                            matlab_channel_dict['B_I'],
                                                            matlab_channel_dict['B_phi'],
                                                            matlab_channel_dict['T'])
            # For CD channels
            dO_I_CD, dD_I_CD, dO_phi_CD, dD_phi_CD = fnirs.preprocess(self.ssy0_CD[0],
                                                            self.ssy0_CD[1],
                                                            matlab_channel_dict['C_I'],
                                                            matlab_channel_dict['C_phi'],
                                                            matlab_channel_dict['D_I'],
                                                            matlab_channel_dict['D_phi'],
                                                            matlab_channel_dict['T'])

            # Reforamt output matlab.double as DataFrame
            preprocessed_chunk = self.matlab_output_to_df(dO_I_AB,
                                                            dD_I_AB,
                                                            dO_phi_AB,
                                                            dD_phi_AB,
                                                            dO_I_CD,
                                                            dD_I_CD,
                                                            dO_phi_CD,
                                                            dD_phi_CD)
            # DF columns now:
            #   ['dO_I_AB', 'dD_I_AB', 'dO_phi_AB', 'dD_phi_AB',
            #    'dO_I_CD', 'dD_I_CD', 'dO_phi_CD', 'dD_phi_CD']

            # Add label, chunk, row_index, timestamp for the preprocessed chunk
            preprocessed_chunk[['chunk', 'row_index', 'timestamp', 'label', 'T']] = \
            chunk_df[['chunk', 'row_index', 'timestamp', 'label', 'T']]
            # DF columns now:
            #   ['chunk', 'row_index', 'timestamp', 'label', 'T',
            #    'dO_I_AB', 'dD_I_AB', 'dO_phi_AB', 'dD_phi_AB',
            #    'dO_I_CD', 'dD_I_CD', 'dO_phi_CD', 'dD_phi_CD']

            # preprocessed_chunk['label'] = chunk_df['label']
            # preprocessed_chunk['chunk'] = chunk_df['chunk']
            # preprocessed_chunk['row_index'] = chunk_df['row_index']
            # preprocessed_chunk['timestamp'] = chunk_df['timestamp']

            # Update the cache dict of preprocessed chunk dict for this setting
            self.preprocessed_chunk_df_dict[index] = preprocessed_chunk

            # Update the new slide window DF for this setting
            self.preprocessed_slide_window_df_dict[self.serial_type][index] = self.preprocessed_slide_window_df_dict[self.serial_type][index]\
                                            .append(preprocessed_chunk)
            self.preprocessed_slide_window_df_dict[self.serial_type][index] = self.preprocessed_slide_window_df_dict[self.serial_type][index].reset_index(drop=True)

            # Update the chunk index
            self.chunk_index_dict[self.serial_type][index] = self.chunk_index_dict[self.serial_type][index] + 1


    def chunk_df_to_dict(self, chunk):
        # chunk columns:
        # ['chunk', 'row_index', 'timestamp', 'label', 'T', ABCD]
        channel_dict = dict()

        channel_dict['A_I'] = chunk.loc[:, self.column_index_A_I].to_numpy().tolist()
        channel_dict['A_phi'] = chunk.loc[:, self.column_index_A_phi].to_numpy().tolist()
        channel_dict['B_I'] = chunk.loc[:, self.column_index_B_I].to_numpy().tolist()
        channel_dict['B_phi'] = chunk.loc[:, self.column_index_B_phi].to_numpy().tolist()
        channel_dict['C_I'] = chunk.loc[:, self.column_index_C_I].to_numpy().tolist()
        channel_dict['C_phi'] = chunk.loc[:, self.column_index_C_phi].to_numpy().tolist()
        channel_dict['D_I'] = chunk.loc[:, self.column_index_D_I].to_numpy().tolist()
        channel_dict['D_phi'] = chunk.loc[:, self.column_index_D_phi].to_numpy().tolist()
        channel_dict['T'] = chunk.loc[:, ['T']].to_numpy().tolist()

        # keys now:
        #   ['A_I', 'A_phi', 'B_I', 'B_phi', 'C_I', 'C_phi', 'D_I', 'D_phi', 'T']

        return channel_dict


    def dict_to_matlab_dict(self, channel_dict):
        matlab_channel_dict = dict()

        for channel_name in channel_dict:
            channel_list = channel_dict[channel_name]
            matlab_channel_dict[channel_name] = fnirs.list_to_matlab(channel_list)

        # keys now:
        #   ['A_I', 'A_phi', 'B_I', 'B_phi', 'C_I', 'C_phi', 'D_I', 'D_phi', 'T']

        return matlab_channel_dict


    def matlab_output_to_df(self, dO_I_AB, dD_I_AB, dO_phi_AB, dD_phi_AB, dO_I_CD, dD_I_CD, dO_phi_CD, dD_phi_CD):
        # Reformat as lists
        dO_I_AB_list = dO_I_AB._data.tolist()
        dD_I_AB_list = dD_I_AB._data.tolist()
        dO_phi_AB_list = dO_phi_AB._data.tolist()
        dD_phi_AB_list = dD_phi_AB._data.tolist()
        dO_I_CD_list = dO_I_CD._data.tolist()
        dD_I_CD_list = dD_I_CD._data.tolist()
        dO_phi_CD_list = dO_phi_CD._data.tolist()
        dD_phi_CD_list = dD_phi_CD._data.tolist()

        chunk_dict = dict()
        chunk_dict['dO_I_AB'] = dO_I_AB_list
        chunk_dict['dD_I_AB'] = dD_I_AB_list
        chunk_dict['dO_phi_AB'] = dO_phi_AB_list
        chunk_dict['dD_phi_AB'] = dD_phi_AB_list
        chunk_dict['dO_I_CD'] = dO_I_CD_list
        chunk_dict['dD_I_CD'] = dD_I_CD_list
        chunk_dict['dO_phi_CD'] = dO_phi_CD_list
        chunk_dict['dD_phi_CD'] = dD_phi_CD_list

        preprocessed_chunk = pd.DataFrame.from_dict(chunk_dict)
        return preprocessed_chunk


    def send_chunks_to_prediction(self):
        for chunk_index in self.preprocessed_chunk_df_dict:
            temp_chunk_df = self.preprocessed_chunk_df_dict[chunk_index]
            self.send_single_chunk(temp_chunk_df)
        self.preprocessed_chunk_df_dict = dict()


    def send_single_chunk(self, chunk_dataframe):
        """Send the chunk to the port on this machine by socket

        Args:
            chunk_dataframe (Pandas DataFrame): The current chunk
            port (int): The port to send data to
        """

        #build socket
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect((socket.gethostname(), self.send_port))
        
        # print("send data type: {}".format(type(chunk_dataframe)))
        # print(chunk_dataframe)
        # print(sys.getsizeof(pickle.dumps(chunk_dataframe)))
        _socket.send(pickle.dumps(chunk_dataframe))

        #get response from server
        # rec = _socket.recv(1024)
        # rec_data = pickle.loads(rec)
        # print(rec_data)
        _socket.close()


    def save_calibration_DF_to_CSV(self, calibration_df):
        calibration_data_file_path = self.raw_data_path + "/fnirs_init.csv"
        calibration_df.to_csv(calibration_data_file_path, index=False)
        print("\n****************************************************")
        print("FNIRS save calibration raw data to CSV")
        print("****************************************************\n")


    #-------------------------- Callable Functions --------------------------

    def calibration_start(self):
        self.calibration_start_row = self.raw_df.shape[0]-1

    def calibration_end(self):
        self.calibration_end_row = self.raw_df.shape[0]-1

        calibration_raw_df = self.raw_df.loc[self.calibration_start_row:self.calibration_end_row, :]

        channel_dict = self.chunk_df_to_dict(calibration_raw_df)
        # columns lost here:
        #   label, chunk, row_index and timestamp

        matlab_channel_dict = self.dict_to_matlab_dict(channel_dict)

        # Init SSY0 for AB
        ssy0_i_AB, ssy0_phi_AB = fnirs.init_ssy0(matlab_channel_dict['A_I'],
                                            matlab_channel_dict['A_phi'],
                                            matlab_channel_dict['B_I'],
                                            matlab_channel_dict['B_phi'],
                                            matlab_channel_dict['T'])
        # Init SSY0 for CD
        ssy0_i_CD, ssy0_phi_CD = fnirs.init_ssy0(matlab_channel_dict['C_I'],
                                            matlab_channel_dict['C_phi'],
                                            matlab_channel_dict['D_I'],
                                            matlab_channel_dict['D_phi'],
                                            matlab_channel_dict['T'])

        # Save SSY0
        self.ssy0_AB = (ssy0_i_AB, ssy0_phi_AB)
        self.ssy0_CD = (ssy0_i_CD, ssy0_phi_CD)

        self.save_calibration_DF_to_CSV(calibration_raw_df)

        print("\n\n")
        print("Init ssy0, using data from row {} to row {}".format(self.calibration_start_row, self.calibration_end_row))
        print()
        print("SSY0 AB i:")
        print(ssy0_i_AB)
        print("size:", ssy0_i_AB.size)
        print()
        print("SSY0 AB phi")
        print(ssy0_phi_AB)
        print("size:", ssy0_phi_AB.size)
        print("\n\n")


    def listen(self):
        """Listen to the USB port, update raw DF and slide window DFs, save raw DF

        1. Listen to the port on the current machine and recieve data from MUSE

        2. Update the slide windows.
            Everytime a full row of values are received, call the
            update_slide_window_df_list()
            function to update slide window variable
        3. Call APIs for data preprocessing
        """

        self.brain_thread = Thread(target=self.brainLoop, args=[])
        self.brain_thread.start()
    

    def start_session(self, session_type):
        """Reset all internal variables for the new session

        1. Set session type
        2. Reset row index
        3. Reset count number list for all slide window settings
        4. Reset all DataFrames

        Args:
            session_type (string): "train"/"test"
        """
        self.session_type = session_type
        self.row_index = 0
        self.init_all_df()
        self.init_chunk_index()


    def update_label(self, label=None, serial_type=None):
        """Set the label same as arg or default label 

        This function is called at the beginning and end of
        every serial. At the beginning, the label would be set
        to bigN for N-back experiment. At the end, the label
        would be reset to default 

        Args:
            label (int, optional): The new label. Defaults to None.
        """
        if label==None:
            self.label = self.default_label
        else:
            self.label = label
        
        if serial_type==None:
            self.serial_type = "task"
        else:
            self.serial_type = serial_type
    

    def save_data_to_CSVs(self):
        """Save all DataFrames to local files for current session
        """
        """Save all DataFrames to local files for current session
        """
        print("****************************************************")

        # Save raw data for the current session
        raw_data_file_path = self.raw_data_path + "/fnirs_"\
                            + self.session_type + ".csv"
        self.raw_df.to_csv(raw_data_file_path, index=False)
        print("create ---- {}".format(raw_data_file_path))

        # Save slide window data
        preprocessed_data_file_path_prefix = self.preprocessed_data_path\
                            + "/fnirs_" + self.session_type

        for serial_type in self.preprocessed_slide_window_df_dict:
            # For each slide window setting
            for index in list(range(len(self.slide_window_params))):
                window_length = self.slide_window_params[index]["window_length"]
                slide_interval = self.slide_window_params[index]["slide_interval"]

                # Select DataFrame for current setting
                preprocessed_slide_window_df = self.preprocessed_slide_window_df_dict[serial_type][index]

                # Save preprocessed slide window data to folder for preprocessed data
                preprocessed_data_file_path = preprocessed_data_file_path_prefix\
                                            + "_" + serial_type\
                                            + "_" + str(window_length)\
                                            + "_" + str(slide_interval)\
                                            + ".csv"

                preprocessed_slide_window_df.to_csv(preprocessed_data_file_path,\
                                    index=False, columns=self.slide_window_column_index)
                print("create ---- {}".format(preprocessed_data_file_path))

        print("FNIRS save data to csv for {} session ".format(self.session_type))
        print("****************************************************")

        ############# Save MATLAB .mat File to Raw Path #############
        chunk = self.raw_df
        channel_dict = dict()
        channel_dict['A_I'] = chunk.loc[:, self.column_index_A_I].to_numpy()
        channel_dict['A_phi'] = chunk.loc[:, self.column_index_A_phi].to_numpy()
        channel_dict['B_I'] = chunk.loc[:, self.column_index_B_I].to_numpy()
        channel_dict['B_phi'] = chunk.loc[:, self.column_index_B_phi].to_numpy()
        channel_dict['C_I'] = chunk.loc[:, self.column_index_C_I].to_numpy()
        channel_dict['C_phi'] = chunk.loc[:, self.column_index_C_phi].to_numpy()
        channel_dict['D_I'] = chunk.loc[:, self.column_index_D_I].to_numpy()
        channel_dict['D_phi'] = chunk.loc[:, self.column_index_D_phi].to_numpy()
        channel_dict['t'] = chunk.loc[:, ['T']].to_numpy()
        channel_dict['lambda'] = np.array([830, 690])
        mat_path = self.raw_data_path + "/fnirs_"+ self.session_type + ".mat"
        savemat(mat_path, channel_dict)


    def stop(self):
        """Stop the fNIRS receiver
        """
        with self.lock:
            self.STOP_FLAG = True
        self.brain_thread.join()

        self.ser.close()

        fnirs.quit_matlab_engine()
        print("disconnected from brain")