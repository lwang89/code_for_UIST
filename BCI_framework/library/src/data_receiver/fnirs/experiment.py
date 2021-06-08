from threading    import Thread, Lock
from pandas       import DataFrame
# from gsr_thread   import empatica_connection
from brain_thread import fnirs_connection
from datetime     import datetime
from os           import listdir

class experiment:
    def __init__(self):
        self.date      = datetime.date(datetime.now())              
        self.pstring   = self.stringify(0 + 1)
        self.tnum      = 0
        
        # self.gsr_connection   = empatica_connection()
        self.brain_connection = fnirs_connection()
              
        # v = input("device connections complete. experiment ready to begin! press enter to start")
        print("\n")
        
    def stringify(self, val):
        if val < 10: val = "0" + str(val)
        else:        val = str(val)
        return val
              
    def stop_trial(self):
        tstring = self.stringify(self.tnum)
        self.sstr = self.pstring + "_" + str(self.date) + "_" + tstring
        # self.gsr_connection.stop_trial(self.sstr)
        self.brain_connection.stop_trial(self.sstr)
        self.tnum += 1
        print("data saved for trial " + str(self.tnum - 1) + "\n")
        return
            
    def start_trial(self):        
        self.brain_connection.start_trial()
        # self.gsr_connection.start_trial()        
        print("trial " + str(self.tnum) + " started!")
        return

    def stop_experiment(self):       
        self.brain_connection.stop_experiment()
        # self.gsr_connection.stop_experiment()
        print("disconnection complete")
        return

if __name__ == '__main__':
    num_trials = 8
   # rest_time = 60
   # act_time  = 300
    e = experiment()
    e.start_trial()
    while e.tnum < num_trials - 1:
        v = input('press enter to stop the trial, save data, and continue')
        e.stop_trial()
        e.start_trial()
    v = input('press enter to stop final trial')
    e.stop_trial()
    e.stop_experiment()
       
