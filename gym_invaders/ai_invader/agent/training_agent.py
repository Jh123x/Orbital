import numpy as np
import gym
import os
import torch
from .baseagent import BaseAgent
from ..util import preprocess_frame,stack_frame

class TrainingAgent(BaseAgent):
    def __init__(self,input_shape ,action_space ,seed ,device
                 ,model, gamma, alpha,tau,batch_size,max_step,
                 env,num_epochs = 0, path = 'model'):
        '''
        batch_size  : minibatch size
        gamma       : discount rate
        alpha       : learn rate
        env         : function to create environment
        path        : directory to save model to
        '''



        super(TrainingAgent,self).__init__(input_shape,action_space, seed, device,model)
        os.makedirs('model', exist_ok=True)
        self.path = os.path.join(os.getcwd(), path)

        self.gamma = gamma
        self.alpha = alpha
        self.batch_size = batch_size
        self.n_steps = 0
        self.max_steps = max_step
        self.tau = tau
        self.preprocessing = input_shape[1:]
        self.num_epochs = num_epochs
        self.scores = []
        try:
            self.env = env()
        except TypeError:
            print('please use environment creation function')
            self.env = env

    def reset(self):
        return self.env.reset()

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

    def save_obj(self,obj, name):
        '''Saves the state dictionary int obj path'''
        torch.save(obj, os.path.join(self.path, name))

    def get_path(self):
        return self.path

    def random_play(self,render= False):
        """Let the ai play randomly"""
        score = 0

        # Reset environment
        self.env.reset()

        # Render graphics if applicable
        self.env.render(render)
        # Game loop
        while True:



            # Sample from action space
            action = self.env.action_space.sample()

            # Do the action and obtain vars
            state, reward, done, _ = self.env.step(action)

            # Increment score
            score += reward

            # If game is done break out of loop
            if done:
                print("Your Score at end of game is: ", self.env.get_score())
                break

        # Close the env
        self.env.close()

    def stack_frames(self, frames, state, is_new=False):

        #preprocess the frame
        frame = preprocess_frame(state, self.preprocessing)

        # Stack the frame
        frames = stack_frame(frames, frame, is_new)

        # Return stacked frames
        return frames
    def train(self, num_epochs):
        '''
        Trains the model given the current trining algorithm
        '''
        raise NotImplementedError

    def eval(self):
        '''
        Takes the trained agent and plays a game using the trained agent
        '''
        raise NotImplementedError
