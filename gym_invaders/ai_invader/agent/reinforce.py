import numpy as np
import torch
import torch.optim as optim
import random
from .baseagent import BaseAgent

class ReinforceAgent(BaseAgent):

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
        super(ReinforceAgent, self).__init__(input_shape,action_space,seed,device,gamma,alpha)

        #Policy Network and feedback loop
        self.policy_net = policy(input_shape,action_space).to(self.device)
        self.optimizer = optim.RMSprop(self.policy_net.parameters(), lr = self.alpha)

        # Memory
        self.log_probs = [] #action memory
        self.rewards = []   #
        self.masks = []
        self.trained = 0
        self.scoreHistory = []

    def step(self, log_prob, reward, done):
        # save experience in memory
        self.log_probs.append(log_prob)
        self.rewards.append(torch.from_numpy(np.array([reward])).to(self.device))
        self.masks.append(torch.from_numpy(np.array([1-done])).to(self.device))

    def action(self,state):
        '''Return action, log_prob for given state as per current policy'''
        state = torch.from_numpy(state).unsqueeze(0).to(self.device)
        action_probs = self.policy_net(state) # forward propagation of the network parameters
        action = action_probs.sample() # samples from the action distribution at random
        log_prob = action_probs.log_prob(action) # returns the value
        return action.item() , log_prob

    def learn(self, *args):

        returns = self.compute_returns(0,self.gamma)
        log_probs = torch.cat(self.log_probs)
        returns = torch.cat(returns).detach()

        loss = -(log_probs * returns).mean()

        #Minimize the loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.reset_memory()

    def reset_memory(self):
        self.log_probs.clear()
        self.rewards.clear()
        self.masks.clear()

    def model_dict(self, episode, scores):
        ''' Takes in the number of episodes played as well as the model weights and scores'''
        self.trained+=episode
        return super(ReinforceAgent, self).model_dict(policy_net=self.policy_net.state_dict(),
                                                      episode = episode+self.trained,
                                                      scores= self.scoreHistory.extend(scores))
    def get_scores(self):
        return self.scoreHistory

    def load_model(self,state_dict):
        if 'policy_net' in state_dict:
            self.policy_net.load_state_dict(state_dict['policy_net'])
            self.policy_net.eval()
            self.trained = state_dict['episode']
        else:
            print('no stored policy')


    def compute_returns(self,next_val, gamma= 0.99):
        '''
        Monte-Carlo Policy Gradient Method (Episodic)
        for each step in the episode t = 0...T-1:
        G<- return from step t
        θ <- θ+α∇_θ logπ_θ (s_t,a_t ) v_t
        '''
        R = next_val
        returns = []
        for step in reversed(range(len(self.rewards))):
            # δ_v=r+ γV_v (s' )- V_v (s)
            R = self.rewards[step] + gamma * R * self.masks[step]
            returns.insert(0,R)
        return returns
