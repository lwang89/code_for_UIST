from threading import Lock, Thread
import serial
import numpy
from pandas import DataFrame
from operator import methodcaller

class fnirs_connection:
    def __init__(self):       
        self.ser = serial.Serial(port='/dev/ttyUSB0',
                                 baudrate=115000, #115200
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.EIGHTBITS)           
        self.lock = Lock()
        self.init_database()

    def init_database(self):
         self.brain_data = DataFrame()

    """main listening thread"""
    def brainLoop(self):
        while not self.STOP_FLAG:                       
            if self.STOP_FLAG: return
            else:
                try:                   
                    byte_packet = self.ser.read_until()
                    packet_list = byte_packet.decode('utf-8').strip().split()
                    packet_list = list(map(methodcaller("split","="), packet_list))
                    if (packet_list == None or len(packet_list) != 49): continue
                    packet = {x[0]: numpy.float64(x[1]) for x in packet_list}
                    if packet is not None and len(packet.keys()) == 49:
                        print("\n*************************************")
                        print("new data in this loop")
                        print(packet)
                        print("*************************************\n")
                        df = DataFrame(packet, index=[0])     
                        self.brain_data = self.brain_data.append(df, ignore_index = True)
                except:
                    print("malformed packet")
                    print(packet)
   
    """client side functions"""    
    def start_trial(self):
        self.STOP_FLAG = False
        self.brain_thread = Thread(target=self.brainLoop, args=[])
        self.brain_thread.start()
        return
            
    def stop_trial(self, pstring):
        with self.lock:
            self.STOP_FLAG = True
        self.brain_thread.join()
        outbrain = open(pstring + ".brain.json", "w")
        self.brain_data.to_json(outbrain)
        outbrain.close()
        self.init_database()
        return
    
    def stop_experiment(self):
        self.ser.close()
        print("disconnected from brain")
        return
