import numpy as np
import torch
import random
from .baseagent import BaseAgent
from ..model import EvolutionaryAI


class EvoAgent(BaseAgent):
    '''
    Wrapper class for Evo Agent Weights in order to use action()
    '''
    def __init__(self,input = (4,120,160), action_space = 6, seed = 0, gamma = 0.99,alpha = 0.0,device = 'cpu'):
        super(EvoAgent, self).__init__(input,action_space,seed,device,gamma,alpha)
        self.model = EvolutionaryAI(input,action_space)

    def action(self,state):
        inp = torch.from_numpy(state).unsqueeze(0).type('torch.FloatTensor').to(self.device)
        output_probs = self.model(inp).detach().cpu().numpy()[0]
        action = np.random.choice(range(self.action_space), 1, p=output_probs).item()
        return action
    def load_model(self, dict):
        self.model.load_state_dict(dict)
        self.model.eval()
