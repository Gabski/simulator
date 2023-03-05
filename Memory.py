
import random
import torch
from torch.autograd import Variable

class Memory(object):
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
    
    def update(self, event):
        self.memory.append(event)
        if len(self.memory) > self.capacity:
            del self.memory[0]
    
    def sample(self, batch_size):
        samples = zip(*random.sample(self.memory, batch_size))
        return map(lambda x: Variable(torch.cat(x, 0)), samples)