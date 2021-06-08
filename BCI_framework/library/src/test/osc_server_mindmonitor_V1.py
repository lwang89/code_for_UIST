from oscpy.server import OSCThreadServer
from time import sleep

import csv
from pathlib import Path
import datetime
import time


osc = OSCThreadServer()
sock = osc.listen(address='192.168.0.36', port=8888, default=True)

open_file_mode = "a"
raw_data_path = Path(__file__).parent / "../../../storage/raw_data/muse.csv"

row_index = 0
row_values = []

start_flag = True
flag_array = [4]

index_description_row = ["row_index", "timestamp"]
index_description_row = index_description_row + ["alpha_TP9", "alpha_AF7", "alpha_AF8", "alpha_TP10", "alpha_Left(TP9 + AF7)", "alpha_Right(TP9 + AF7)", "alpha_Front(AF7 + AF8)", "alpha_Back(TP9 + AF10)", "alpha_Average"]
index_description_row = index_description_row + ["beta_TP9", "beta_AF7", "beta_AF8", "beta_TP10", "beta_Left(TP9 + AF7)", "beta_Right(TP9 + AF7)", "beta_Front(AF7 + AF8)", "beta_Back(TP9 + AF10)", "beta_Average"]
index_description_row = index_description_row + ["delta_TP9", "delta_AF7", "delta_AF8", "delta_TP10", "delta_Left(TP9 + AF7)", "delta_Right(TP9 + AF7)", "delta_Front(AF7 + AF8)", "delta_Back(TP9 + AF10)", "delta_Average"]
index_description_row = index_description_row + ["theta_TP9", "theta_AF7", "theta_AF8", "theta_TP10", "theta_Left(TP9 + AF7)", "theta_Right(TP9 + AF7)", "theta_Front(AF7 + AF8)", "theta_Back(TP9 + AF10)", "theta_Average"]
index_description_row = index_description_row + ["gamma_TP9", "gamma_AF7", "gamma_AF8", "gamma_TP10", "gamma_Left(TP9 + AF7)", "gamma_Right(TP9 + AF7)", "gamma_Front(AF7 + AF8)", "gamma_Back(TP9 + AF10)", "gamma_Average"]

with open(raw_data_path, open_file_mode) as file:
    writer = csv.writer(file)
    writer.writerow(index_description_row)



'''

https://mind-monitor.com/FAQ.php

Item	            OSC Path	                        Values	        Description	                                Range / Units	            Data rate
RAW EEE	            /muse/eeg	                        f f f f {+f}	TP9, AF7, AF8, TP10 {+AUX on MU-02/MU-03}	0.0 - 1682.815 uV	        220Hz | 256Hz
Delta Absolute	    /muse/elements/delta_absolute	    f | f f f f	    One Average or Four Float values	        Bels	                    10Hz
Theta Absolute	    /muse/elements/theta_absolute	    f | f f f f	    One Average or Four Float values	        Bels	                    10Hz
Alpha Absolute	    /muse/elements/alpha_absolute	    f | f f f f	    One Average or Four Float values	        Bels	                    10Hz
Beta Absolute	    /muse/elements/beta_absolute	    f | f f f f	    One Average or Four Float values	        Bels	                    10Hz
Gamma Absolute	    /muse/elements/gamma_absolute	    f | f f f f	    One Average or Four Float values	        Bels	                    10Hz
Horseshoe	        /muse/elements/horseshoe	        f f f f	        TP9, AF7, AF8, TP10 fit	                    1=Good, 2=Medium, 4=Bad	    10Hz
Touching Forehead	/muse/elements/touching_forehead	i	            Forehead fit	                            1=True, 0=False	            10Hz
Battery info	    /muse/batt	                        i i i i	        Batt Level, Batt Voltage, ADC Voltage, Temp	%/100, mV, {-1 N/A}, C	    0.1Hz
Gyroscope	        /muse/gyro	                        f f f	        X, Y, Z	                                    degrees/second {-245:+245}	52Hz
Accelerometer	    /muse/acc	                        f f f	        X, Y, Z	                                    g {-2:+2}	                52Hz
Blink	            /muse/elements/blink	            i	            Blink detected	                            1=Blink	                    10Hz (if true)
Jaw Clench	        /muse/elements/jaw_clench	        i	            Jaw Clench detected	                        1=Jaw Clench	            10Hz (if true)
Markers	            /Marker/{1,2,3,4,5}	                i	            Marker Button Pressed	                    1=True	                    Instant

'''

### Mind Monitor
'''
@osc.address(b'/muse/eeg')
def callback(*values):
    t = datetime.datetime.now()
    string = "eeg                              got values: {}\n".format(values)
    string = str(t) + ", " + string
    print(string)
    with open(raw_data_path, open_file_mode) as file:
        file.write(string)
        file.flush()

@osc.address(b'/muse/gyro')
def callback(*values):
    t = datetime.datetime.now()
    string = "gyro                             got values: {}\n".format(values)
    string = str(t) + ", " + string
    print(string)
    with open(raw_data_path, open_file_mode) as file:
        file.write(string)
        file.flush()

@osc.address(b'/muse/elements/touching_forehead')
def callback(*values):
    t = datetime.datetime.now()
    string = "touching_forehead                got values: {}\n".format(values)
    string = str(t) + ", " + string
    print(string)
    with open(raw_data_path, open_file_mode) as file:
        file.write(string)
        file.flush()
'''
@osc.address(b'/muse/elements/alpha_absolute')
def callback(*values):
    global row_index, row_values, start_flag, flag_array

    t = int(round(time.time() * 1000))

    values = list(values)
    if len(values)<4:
        print("Less than 4 features")
        print("alpha_absolute")
        print(values)
        return 0
    
    if (flag_array[-1] != 4):
        print("gamma not follows theta")
        print(flag_array)
    flag_array = [0]

    values.append(values[0] + values[1])    # Left: TP9 + AF7
    values.append(values[2] + values[3])    # Right: TP10 + AF8
    values.append(values[1] + values[2])    # Front: AF7 + AF8
    values.append(values[0] + values[3])    # Back: TP9 + TP10
    values.append((values[0] + values[1] + values[2] + values[3])/4)    # Average
    row_values = [row_index, t] + values
    row_index = row_index + 1


@osc.address(b'/muse/elements/beta_absolute')
def callback(*values):
    global row_index, row_values, start_flag, flag_array

    t = int(round(time.time() * 1000))
    
    values = list(values)
    if len(values)<4:
        print("Less than 4 features")
        print("beta_absolute")
        print(values)
        return 0

    if (flag_array[-1] != 0):
        print("beta not follows alpha")
        print(flag_array)
    flag_array.append(1)

    values.append(values[0] + values[1])    # Left: TP9 + AF7
    values.append(values[2] + values[3])    # Right: TP10 + AF8
    values.append(values[1] + values[2])    # Front: AF7 + AF8
    values.append(values[0] + values[3])    # Back: TP9 + TP10
    values.append((values[0] + values[1] + values[2] + values[3])/4)    # Average
    row_values = row_values + values


@osc.address(b'/muse/elements/delta_absolute')
def callback(*values):
    global row_index, row_values, start_flag, flag_array

    t = int(round(time.time() * 1000))

    values = list(values)
    if len(values)<4:
        print("Less than 4 features")
        print("delta_absolute")
        print(values)
        return 0

    if (flag_array[-1] != 1):
        print("delta not follows beta")
        print(flag_array)
    flag_array.append(2)

    values.append(values[0] + values[1])    # Left: TP9 + AF7
    values.append(values[2] + values[3])    # Right: TP10 + AF8
    values.append(values[1] + values[2])    # Front: AF7 + AF8
    values.append(values[0] + values[3])    # Back: TP9 + TP10
    values.append((values[0] + values[1] + values[2] + values[3])/4)    # Average
    row_values = row_values + values


@osc.address(b'/muse/elements/theta_absolute')
def callback(*values):
    global row_index, row_values, start_flag, flag_array

    t = int(round(time.time() * 1000))

    values = list(values)
    if len(values)<4:
        print("Less than 4 features")
        print("theta_absolute")
        print(values)
        return 0

    if (flag_array[-1] != 2):
        print("theta not follows delta")
        print(flag_array)
    flag_array.append(3)

    values.append(values[0] + values[1])    # Left: TP9 + AF7
    values.append(values[2] + values[3])    # Right: TP10 + AF8
    values.append(values[1] + values[2])    # Front: AF7 + AF8
    values.append(values[0] + values[3])    # Back: TP9 + TP10
    values.append((values[0] + values[1] + values[2] + values[3])/4)    # Average
    row_values = row_values + values


@osc.address(b'/muse/elements/gamma_absolute')
def callback(*values):
    global row_index, row_values, start_flag, flag_array

    t = int(round(time.time() * 1000))

    values = list(values)
    if len(values)<4:
        print("Less than 4 features")
        print("gamma_absolute")
        print(values)
        return 0

    if (flag_array[-1] != 3):
        print("gamma not follows theta")
        print(flag_array)
    flag_array.append(4)

    values.append(values[0] + values[1])    # Left: TP9 + AF7
    values.append(values[2] + values[3])    # Right: TP10 + AF8
    values.append(values[1] + values[2])    # Front: AF7 + AF8
    values.append(values[0] + values[3])    # Back: TP9 + TP10
    values.append((values[0] + values[1] + values[2] + values[3])/4)    # Average
    row_values = row_values + values

    with open(raw_data_path, open_file_mode) as file:
        writer = csv.writer(file)
        writer.writerow(row_values)
        row_values = []



'''
@osc.address(b'/muse/elements/horseshoe')
def callback(*values):
    t = datetime.datetime.now()
    string = "horseshoe                        got values: {}\n".format(values)
    string = str(t) + ", " + string
    print(string)
    with open(raw_data_path, open_file_mode) as file:
        file.write(string)
        file.flush()

@osc.address(b'/muse/batt')
def callback(*values):
    t = datetime.datetime.now()
    string = "batt                             got values: {}\n".format(values)
    string = str(t) + ", " + string
    print(string)
    with open(raw_data_path, open_file_mode) as file:
        file.write(string)
        file.flush()

@osc.address(b'/muse/elements/jaw_clench')
def callback(*values):
    t = datetime.datetime.now()
    string = "jaw_clench                       got values: {}\n".format(values)
    string = str(t) + ", " + string
    print(string)
    with open(raw_data_path, open_file_mode) as file:
        file.write(string)
        file.flush()

@osc.address(b'/muse/elements/blink')
def callback(*values):
    t = datetime.datetime.now()
    string = "blink                            got values: {}\n".format(values)
    string = str(t) + ", " + string
    print(string)
    with open(raw_data_path, open_file_mode) as file:
        file.write(string)
        file.flush()
'''
while True:
    sleep(1000)
osc.stop()