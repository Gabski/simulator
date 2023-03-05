import torch.nn as nn
import torch.nn.functional as Funcional

class Network(nn.Module):
    
    def __init__(self, inputSize, outputSize):
        super(Network, self).__init__()
        self.outputSize = outputSize
        self.inputSize = inputSize
        self.layerIn = nn.Linear(inputSize, 30)
        self.layerOut = nn.Linear(30, outputSize)
    
    def forward(self, state):
        x = Funcional.relu(self.layerIn(state))
        return self.layerOut(x)
        
