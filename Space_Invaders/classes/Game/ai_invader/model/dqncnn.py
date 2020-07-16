import torch
from . import BaseModel

class DQNCNN(BaseModel):
    '''
    DQN CNN Model to pass frames through for feature detection
    '''
    def __init__(self, input_shape, num_actions):
        """Base DQN class"""
        super().__init__(input_shape, num_actions)
        self.fc = torch.nn.Sequential(
            torch.nn.Linear(self.feature_size(), 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, self.num_actions)
        )