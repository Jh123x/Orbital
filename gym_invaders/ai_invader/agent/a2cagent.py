import numpy as np

import torch
import torch.nn as nn
from torch.optim import Adam, RMSprop
from .baseagent import BaseAgent
from ..model.actor_critic import Actor,Critic
from ..util import ReplayMemory

class A2C(BaseAgent):
    def __init__(self, input_shape,action_space, seed, device, gamma, alpha,
                 memsize,batch_size,roll_out_n_steps = 10):
        super(A2C, self).__init__(input_shape,action_space,seed,device,gamma,alpha)
        self.memory = ReplayMemory(memsize,batch_size,seed,device)
        self.roll
