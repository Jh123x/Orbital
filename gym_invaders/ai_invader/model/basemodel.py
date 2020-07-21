import torch
import torch.nn as nn
import torch.autograd as autograd

class BaseModel(nn.Module):
    def __init__(self, input_shape, num_actions):
        super(BaseModel, self).__init__()
        self.input_shape = input_shape
        self.num_actions = num_actions
        self.features = nn.Sequential(
            nn.Conv2d(input_shape[0],32,kernel_size=8,stride=4),
            nn.ReLU(),
            nn.Conv2d(32,64,kernel_size=4,stride=2),
            nn.ReLU(),
            nn.Conv2d(64,64,kernel_size=3,stride=1),
            nn.ReLU()
        )
        self.fc = nn.Sequential(
            nn.Linear(self.feature_size(), 512),
            nn.ReLU(),
            nn.Linear(512, self.num_actions),
            nn.Softmax(dim=1)
        )

    def forward(self,x):
        ''' Will be overloaded by default'''
        raise NotImplementedError('Did not implement function that should be implemented')

    def feature_size(self):
        '''Unravels the model inputs'''
        return self.features(autograd.Variable(torch.zeros(1,*self.input_shape))).view(1,-1).size(1)
