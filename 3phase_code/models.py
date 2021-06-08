## Description: we store the two models here (LR and CNN)

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

class SimpleCNN(nn.Module):
    def __init__(self, input_size, conv1d_hidden_size, window_size, window_stride, linear_hidden_size, num_classes):

        super(SimpleCNN, self).__init__()
        
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
