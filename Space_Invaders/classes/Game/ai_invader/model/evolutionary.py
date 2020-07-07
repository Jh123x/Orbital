import torch.nn as nn
from .basemodel import BaseModel

class EvolutionaryAI(BaseModel):
    def __init__(self, input_shape, num_actions):
        """Base Evolution class"""
        super().__init__(input_shape,num_actions)
        self.fc = nn.Sequential(
            nn.Linear(self.feature_size(),512),
            nn.LeakyReLU(),
            nn.Linear(512,self.num_actions),
            nn.Softmax(dim=1)
        )
