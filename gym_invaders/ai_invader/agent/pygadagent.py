from numpy.random import choice
from ..model import PyGADModel

class PyGadAgent():
    def __init__(self, input_shape,action_size):
        self.input_shape = input_shape
        self.action_size = action_size
        self.model = PyGADModel(input_shape,action_size)

    def action(self,state):
        '''
        Takes an action based on current state and current policy
        '''
        output_probs = self.model.forward(state)
        output_action = choice(range(self.action_size),p=output_probs)
        return output_action

