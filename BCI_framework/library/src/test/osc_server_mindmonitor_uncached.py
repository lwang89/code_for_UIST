from oscpy.server import OSCThreadServer
from time import sleep

import csv
from pathlib import Path
import datetime
import time


osc = OSCThreadServer()
sock = osc.listen(address='192.168.0.36', port=8888, default=True)

open_file_mode = "a"
raw_data_path = Path(__file__).parent / "../../../storage/raw_data/muse_uncached.csv"

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
    #t = datetime.datetime.now()
    t = int(round(time.time() * 1000))
    #string = "alpha_absolute                   got values: {}\n".format(values)
    values = list(values)
    if len(values)<4:
        print("Less than 4 features")
        print("alpha_absolute")
        print(values)
        return 0

    values.append(values[0] + values[1])    # Left: TP9 + AF7
    values.append(values[2] + values[3])    # Right: TP10 + AF8
    values.append(values[1] + values[2])    # Front: AF7 + AF8
    values.append(values[0] + values[3])    # Back: TP9 + AF10
    values.append(values[0] + values[1] + values[2] + values[3])    # Sum
    values.insert(0, t)                     # TimeStamp
    values.insert(0, 0)                     # ID = 0, alpha_absolute
    #string = str(t) + ", " + "{}\n".format(values)
    
    with open(raw_data_path, open_file_mode) as file:
        writer = csv.writer(file)
        writer.writerow(values)
    
    '''
        file.write(string)
        file.flush()
    '''

@osc.address(b'/muse/elements/beta_absolute')
def callback(*values):
    #t = datetime.datetime.now()
    t = int(round(time.time() * 1000))
    #string = "beta_absolute                    got values: {}\n".format(values)
    values = list(values)
    if len(values)<4:
        print("Less than 4 features")
        print("beta_absolute")
        print(values)
        return 0

    values.append(values[0] + values[1])    # Left: TP9 + AF7
    values.append(values[2] + values[3])    # Right: TP10 + AF8
    values.append(values[1] + values[2])    # Front: AF7 + AF8
    values.append(values[0] + values[3])    # Back: TP9 + AF10
    values.append(values[0] + values[1] + values[2] + values[3])    # Sum
    values.insert(0, t)                     # TimeStamp
    values.insert(0, 1)                     # ID = 1, beta_absolute
    #string = str(t) + ", " + "{}\n".format(values)
    
    with open(raw_data_path, open_file_mode) as file:
        writer = csv.writer(file)
        writer.writerow(values)
    
    '''
        file.write(string)
        file.flush()
    '''

@osc.address(b'/muse/elements/delta_absolute')
def callback(*values):
    #t = datetime.datetime.now()
    t = int(round(time.time() * 1000))
    #string = "delta_absolute                   got values: {}\n".format(values)
    values = list(values)
    if len(values)<4:
        print("Less than 4 features")
        print("delta_absolute")
        print(values)
        return 0

    values.append(values[0] + values[1])    # Left: TP9 + AF7
    values.append(values[2] + values[3])    # Right: TP10 + AF8
    values.append(values[1] + values[2])    # Front: AF7 + AF8
    values.append(values[0] + values[3])    # Back: TP9 + AF10
    values.append(values[0] + values[1] + values[2] + values[3])    # Sum
    values.insert(0, t)                     # TimeStamp
    values.insert(0, 2)                     # ID = 2, delta_absolute
    #string = str(t) + ", " + "{}\n".format(values)
    
    with open(raw_data_path, open_file_mode) as file:
        writer = csv.writer(file)
        writer.writerow(values)
    
    '''
        file.write(string)
        file.flush()
    '''

@osc.address(b'/muse/elements/theta_absolute')
def callback(*values):
    #t = datetime.datetime.now()
    t = int(round(time.time() * 1000))
    #string = "theta_absolute                   got values: {}\n".format(values)
    values = list(values)
    if len(values)<4:
        print("Less than 4 features")
        print("theta_absolute")
        print(values)
        return 0

    values.append(values[0] + values[1])    # Left: TP9 + AF7
    values.append(values[2] + values[3])    # Right: TP10 + AF8
    values.append(values[1] + values[2])    # Front: AF7 + AF8
    values.append(values[0] + values[3])    # Back: TP9 + AF10
    values.append(values[0] + values[1] + values[2] + values[3])    # Sum
    values.insert(0, t)                     # TimeStamp
    values.insert(0, 3)                     # ID = 3, theta_absolute
    #string = str(t) + ", " + "{}\n".format(values)
    
    with open(raw_data_path, open_file_mode) as file:
        writer = csv.writer(file)
        writer.writerow(values)
    
    '''
        file.write(string)
        file.flush()
    '''

@osc.address(b'/muse/elements/gamma_absolute')
def callback(*values):
    #t = datetime.datetime.now()
    t = int(round(time.time() * 1000))
    #string = "gamma_absolute                   got values: {}\n".format(values)
    values = list(values)
    if len(values)<4:
        print("Less than 4 features")
        print("gamma_absolute")
        print(values)
        return 0

    values.append(values[0] + values[1])    # Left: TP9 + AF7
    values.append(values[2] + values[3])    # Right: TP10 + AF8
    values.append(values[1] + values[2])    # Front: AF7 + AF8
    values.append(values[0] + values[3])    # Back: TP9 + AF10
    values.append(values[0] + values[1] + values[2] + values[3])    # Sum
    values.insert(0, t)                     # TimeStamp
    values.insert(0, 4)                     # ID = 4, gamma_absolute
    #string = str(t) + ", " + "{}\n".format(values)

    with open(raw_data_path, open_file_mode) as file:
        writer = csv.writer(file)
        writer.writerow(values)

    '''
        file.write(string)
        file.flush()
    '''


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