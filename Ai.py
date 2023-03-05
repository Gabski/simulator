import torch
import torch.nn.functional as Funcional
import torch.optim as optim
from torch.autograd import Variable
from Memory import Memory
from Network import Network
import os

class Ai():
    
    def __init__(self, inputSize, nbAction, gamma):
        self.gamma = gamma
        self.rewardWindow = []
        self.model = Network(inputSize, nbAction)
        self.memory = Memory(1000)
        self.optimizer = optim.Adam(self.model.parameters(), lr = 0.001)
        self.lastState = torch.Tensor(inputSize).unsqueeze(0)
        self.lastAction = 0
        self.lastReward = 0
    
    def _selectAction(self, state):
        probs = Funcional.softmax(self.model(Variable(state))*100) 
        action = probs.multinomial(1)
        return action.data[0,0]
    
    def _learn(self, batchState, batchNextState, batchReward, batchAction):
        outputs = self.model(batchState).gather(1, batchAction.unsqueeze(1)).squeeze(1)
        nextOutputs = self.model(batchNextState).detach().max(1)[0]
        target = self.gamma * nextOutputs + batchReward
        tdLoss = Funcional.smooth_l1_loss(outputs, target)
        self.optimizer.zero_grad()
        tdLoss.backward()
        self.optimizer.step()
    
    def update(self, reward, newSignal):
        newState = torch.Tensor(newSignal).float().unsqueeze(0)
        self.memory.update((self.lastState, newState, torch.LongTensor([int(self.lastAction)]), torch.Tensor([self.lastReward])))
        action = self._selectAction(newState)
        if len(self.memory.memory) > 100:
            batchState, batchNextState, batchAction, batchReward = self.memory.sample(100)
            self._learn(batchState, batchNextState, batchReward, batchAction)
        self.lastAction = action
        self.lastState = newState
        self.lastReward = reward
        self.rewardWindow.append(reward)
        if len(self.rewardWindow) > 1000:
            del self.rewardWindow[0]

        return action
    
    def score(self):
        return sum(self.rewardWindow)/(len(self.rewardWindow)+1.)

    def save(self):
        torch.save({'state': self.model.state_dict(), 'opti' : self.optimizer.state_dict()}, 'save.pth')
    
    def load(self):
        if os.path.isfile('save.pth'):
            checkpoint = torch.load('save.pth')
            self.model.load_state_dict(checkpoint['state'])
            self.optimizer.load_state_dict(checkpoint['opti'])
     