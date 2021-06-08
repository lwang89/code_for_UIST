import matlab.engine

ENG = None

def init_matlab_engine():
    global ENG
    ENG = matlab.engine.start_matlab()
    ENG.addpath('./library/src/data_preprocessing/fnirs', nargout=0)


def quit_matlab_engine():
    global ENG
    ENG.quit()


def list_to_matlab(value_list):
    matlab_object = matlab.double(value_list)
    return matlab_object


def preprocess(ssy0_I, ssy0_phi, A_I, A_phi, B_I, B_phi, T):
    dO_I, dD_I, dO_phi, dD_phi = ENG.preprocess(ssy0_I, ssy0_phi, A_I, A_phi, B_I, B_phi, T, nargout=4)
    return dO_I, dD_I, dO_phi, dD_phi


def init_ssy0(A_I, A_phi, B_I, B_phi, T):
    global ENG
    ssy0_i, ssy0_phi = ENG.init_ssy0(A_I, A_phi, B_I, B_phi, T, nargout=2)
    return ssy0_i, ssy0_phi