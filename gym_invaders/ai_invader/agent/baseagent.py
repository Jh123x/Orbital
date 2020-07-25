import random
import numpy as np

class BaseAgent():
    def __init__(self, input_shape,action_space, seed, device, model):
        self.input_shape = input_shape
        self.action_space = action_space
        self.seed = seed
        self.device = device
        self.model = model


    def step(self, *args):
        '''
        Takes one step
        Expected Args:
        state: stacked_frames of current state
        action: action taken
        reward: Reward from action
        next_state: The following state after action was taken
        done: Is the state done.
        '''
        raise NotImplementedError

    def learn(self,state):
        '''
        Learns from the state via backpropagation
        '''
        raise NotImplementedError

    # choose an action based on state with random noise added for exploration in training
    def exploration_action(self, state):
        pass

    def action(self,state):
        ''' Takes a action based on the state
        - Not Implemented: Takes a random sample and returns a random action
        '''
        return random.sample(range(self.action_space))

    def value(self,state, action):
        pass

    def discounted_reward(self, rewards, final_value):
        discounted_r = np.zeros_like(rewards)
        running_add = final_value
        for t in reversed(range(0,len(rewards))):
            running_add = running_add * self.gamma + rewards[t]
            discounted_r[t] = running_add
        return discounted_r

    def soft_update_tgt(self, tgt, src):
        '''
        soft update the actor tgt or critic tgt network
        '''
        for t,s in zip(tgt.parameters(), src.parameters()):
            t.data.copy_(
                (1. - self.tau) * t.data + self.tau * s.data)

    def model_dict(self,**kwargs):
        diction = {}
        for k,v in kwargs.items():
            diction[k] = v
        return diction

    def load_model(self, dict):
        raise NotImplementedError
