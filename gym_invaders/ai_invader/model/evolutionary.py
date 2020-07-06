import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from .basemodel import BaseModel

class EvolutionaryAI(BaseModel):
    def __init__(self, input_shape, num_actions):
        super(EvolutionaryAI,self).__init__(input_shape,num_actions)
        self.fc = nn.Sequential(
            nn.Linear(self.feature_size(),512),
            nn.LeakyReLU(),
            nn.Linear(512,self.num_actions),
            nn.Softmax(dim=1)
        )

    def forward(self,x):
        x = self.features(x)
        x = x.view(x.size(0),-1)
        x = self.fc(x)
        return x
