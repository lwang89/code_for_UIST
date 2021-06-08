import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


class LogisticRegression(nn.Module):
    def __init__(self, input_dim, num_classes):
        super(LogisticRegression, self).__init__()
        self.linear = torch.nn.Linear(input_dim, num_classes)
        
    def forward(self, x):
        outputs = self.linear(x)
        return outputs
    

    
class BiRNN(nn.Module):

    def __init__(self, input_size, hidden_size, num_layers, num_classes, num_directions = 1, device = 'cpu'):
        super(BiRNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.num_directions = num_directions #June17 added
        self.device = device
        
        if num_directions == 1:
            bidirectional_flag = False
        elif num_directions == 2:
            bidirectional_flag = True
        
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers,
                            batch_first=True, bidirectional=bidirectional_flag)
        self.dropout1 = nn.Dropout(p=0.2) #inplace: dafualt False
        self.fc = nn.Linear(self.hidden_size*self.num_directions, self.num_classes)

        
    def forward(self, x):

        out, _ = self.lstm(x)
        
        out = torch.sum(out, dim=1)
        
        out = self.dropout1(out)
        
        # output layer
        out = F.log_softmax(self.fc(out), dim=1)
        
        return out
    
    
class SimpleRNN(nn.Module):
     
    def __init__(self, input_size, hidden_size, num_layers, num_classes, num_directions = 1, device = 'cpu'):
        super(SimpleRNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.num_directions = num_directions #June17 added
        self.device = device
    
        if num_directions == 1:
            bidirectional_flag = False
        elif num_directions == 2:
            bidirectional_flag = True
        

        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True, bidirectional = bidirectional_flag)
        self.dropout1 = nn.Dropout(p=0.2) #inplace: dafualt False
        self.fc = nn.Linear(self.hidden_size*self.num_directions, self.num_classes)

        

    def forward(self, x):
        
        out, _ = self.rnn(x)
        
        out = torch.sum(out, dim=1)
        
        out = self.dropout1(out)
                
        out = F.log_softmax(self.fc(out), dim=1)
        
        return out
    



class CNN(nn.Module):
    def __init__(self, input_size, conv1d_hidden_size, window_size, window_stride, linear_hidden_size, num_classes):

        super(CNN, self).__init__()
        
        self.conv1d_hidden_size =  conv1d_hidden_size #hidden_size is the num out_channel for Conv1d
        self.input_size = input_size #input_size is the feature size at each time step
        self.window_size = window_size #window_size is the kernel size of Conv1d
        self.window_stride = window_stride #window_stride is the stride for Conv1d
        self.linear_hidden_size = linear_hidden_size
        self.num_classes = num_classes
        
        
        self.conv1d = nn.Conv1d(in_channels = input_size, out_channels = conv1d_hidden_size, kernel_size = window_size, stride = window_stride, padding = 0, padding_mode = 'zeros', dilation = 1, groups = 1, bias = True) 
        #Default: padding=0,  padding_mode='zeros', dilation=1, groups=1, bias=True
        self.fc1 = nn.Linear(in_features = conv1d_hidden_size, out_features = linear_hidden_size, bias = True)
        self.fc2 = nn.Linear(in_features = linear_hidden_size, out_features = num_classes, bias = True)
        self.dropout = nn.Dropout(p=0.2, inplace=False)
       
        

    def forward(self, x):
        conv1d_out = self.conv1d(x.transpose(1,2)) #pytorch conv1d slide from left to right instead of top to down in tf
        
        conv1d_out = torch.sum(conv1d_out, dim = -1)
        
        fc1_out = self.fc1(conv1d_out)
        
        fc1_out = F.relu(fc1_out)
        
        fc1_out = self.dropout(fc1_out)
        
       
        fc2_out = self.fc2(fc1_out)
        
        logits = F.log_softmax(fc2_out, dim = 1)        

        return logits
