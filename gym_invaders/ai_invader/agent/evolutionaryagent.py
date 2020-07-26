import numpy as np
import torch
from . import BaseAgent
from ..model import EvolutionaryAI

class EvoAgent(BaseAgent):
    '''
    Wrapper class for Evo Agent Weights in order to use action()
    '''
    def __init__(self,input = (4,120,160), action_space = 6, seed = 0,device = 'cpu',model= EvolutionaryAI):
        super(EvoAgent, self).__init__(input,action_space,seed,device,model)
        self.evo = self.model(self.input_shape,self.action_space)

    def action(self,state):
        inp = torch.from_numpy(state).unsqueeze(0).type('torch.FloatTensor').to(self.device)
        output_probs = self.model(inp).detach().cpu().numpy()[0]
        action = np.random.choice(range(self.action_space), 1, p=output_probs).item()
        return action
    def load_model(self, diction):
        '''
        Loading Model from state dictionary
        '''
        self.evo.load_state_dict(diction)
        self.evo.eval()
