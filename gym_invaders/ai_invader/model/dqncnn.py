import torch.nn as nn
from .basemodel import BaseModel

class DQNCNN(BaseModel):
    '''
    DQN CNN Model to pass frames through for feature detection
    '''
    def __init__(self, input_shape, num_actions):
        super(DQNCNN, self).__init__(input_shape,num_actions )
        self.fc = nn.Sequential(
            nn.Linear(self.feature_size(), 512),
            nn.LeakyReLU(),
            nn.Linear(512, self.num_actions)
        )

    def forward(self, x):
        # print(x)
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

