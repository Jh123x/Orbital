import torch
from .basemodel import BaseModel

class EvolutionaryAI(BaseModel):
    def __init__(self, input_shape, num_actions):
        """Base Evolution class"""
        super().__init__(input_shape,num_actions)
        self.fc = torch.nn.Sequential(
            torch.nn.Linear(self.feature_size(),512),
            torch.nn.LeakyReLU(),
            torch.nn.Linear(512,self.num_actions),
            torch.nn.Softmax(dim=1)
        )
