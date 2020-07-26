import random
import numpy as np

class BaseAgent():
    def __init__(self, input_shape,action_space, seed, device, model):
        '''
        Base Class of Agent:
        Agents to be incorporated into game should inherit from this class
        Role: Forward propagation of model to produce a target action.
        input_shape : dimensions of each state(C, H, W)
        action space : dimension of each action
        seed        : random seed
        device     : Using GPU or CPU
        batch_size  : minibatch size
        model     : Pytorch Model
        '''
        self.input_shape = input_shape
        self.action_space = action_space
        self.seed = seed
        self.device = device
        self.model = model

    def action(self,state):
        ''' Takes a action based on the state
        - Not Implemented: Takes a random sample and returns a random action
        '''
        return random.sample(range(self.action_space))

    def load_model(self, dict,eval= True):
        '''
        load a state dict into the model
        if eval mode, no training of layers occur
        '''
        raise NotImplementedError