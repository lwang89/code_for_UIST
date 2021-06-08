from ..streaming_data_receiver.Muse.osc_server_mindmonitor_binding_directly import muse_receiver
#import numpy as np
mr = muse_receiver()
mr.write_index()
mr.listen()
mr.stop()
