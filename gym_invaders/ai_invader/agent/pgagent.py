import numpy as np
import torch
import torch.nn.functional as F
import torch.optim as optim
import random

class ReinforceAgent():

    def __init__(self, input_shape, action_space, seed, device, gamma, alpha, policy):
        '''
            Policy Gradient Network Agent using REINFORCE algorithm
            Parameters:
                Input_shape: Dimension of state
                Action_space: dimension of action space
                Seed: random seed
                Device: GPU/CPU
                gamma: Discount factor
                alpha: learning rate
                policy: Policy Network
        '''
        self.input_shape = input_shape
        self.action_space = action_space
        self.seed = random.seed(seed)
        self.device = device
        self.alpha = alpha
        self.gamma = gamma

        #Policy Network and feedback loop
        self.policy_net = policy(input_shape,action_space).to(self.device)
        self.optimizer = optim.