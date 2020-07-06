import random

class BaseAgent():
    def __init__(self, input, action_space, seed, device,gamma,alpha):
        self.input_shape = input
        self.action_space = action_space
        self.seed = random.seed(seed)
        self.device= device
        self.gamma = gamma
        self.alpha = alpha

    def step(self, *args):
        raise NotImplementedError

    def action(self,*args):
        return random.sample(range(self.action_space))

    def learn(self, state):
        raise NotImplementedError

    def model_dict(self,**kwargs):
        diction = {}
        for k,v in kwargs.items():
            diction[k] = v
        return diction

    def load_model(self, dict):
        raise NotImplementedError
