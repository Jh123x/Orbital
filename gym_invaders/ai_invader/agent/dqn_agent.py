import numpy.random as rand
import torch.nn.functional as F
import torch.optim as optim
import random
import torch
import numpy as np
from ..util.memory import *


class DQNAgent():
    def __init__(self, input_shape, action_size, seed, device, buffer_size, batch_size,
                 gamma, alpha, tau, update, replay, model):
        '''Initialise a Agent Object
        input_shape : dimensions of each state(C, H, W)
        action size : dimension of each action
        seed        : random seed
        device.     : Using GPU or CPU
        buffer_size : size of replay buffer
        batch_size  : minibatch size
        gamma       : discount rate
        alpha       : learn rate
        update      : update interval
        replay.     : after which replay to be started
        model.      : Pytorch Model
        '''
        self.input_shape = input_shape
        self.action_size = action_size
        self.seed = random.seed(seed)
        self.device = device
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.gamma = gamma
        self.alpha = alpha
        self.update = update
        self.replay = replay
        self.DQN = model
        self.tau = tau

        # Q-Network
        self.policy_net = self.DQN(input_shape, action_size).to(self.device)
        self.target_net = self.DQN(input_shape, action_size).to(self.device)
        self.optimiser = optim.RMSprop(self.policy_net.parameters(), lr=self.alpha)
        # Replay Memory
        self.memory = ReplayMemory(self.buffer_size, self.batch_size, self.seed, self.device)
        # Timestep
        self.t_step = 0

    def step(self, state, action, reward, next_state, done):

        # Save experience into replay buffer
        self.memory.add(state, action, reward, next_state, done)

        # Learn every update % timestep
        # print(self.t_step)

        self.t_step = (self.t_step + 1) % self.update

        # print(self.t_step)
        if self.t_step == 0:
            # if there are enough samples in the memory, get a random subset and learn
            if len(self.memory) > self.replay:
                experience = self.memory.sample()
                self.learn(experience)

    def action(self, state, eps=0.):
        ''' Returns action for given state as per current policy'''
        #Unpack the state
        state = torch.from_numpy(state).unsqueeze(0).to(self.device)

        #Evaluate the policy
        self.policy_net.eval()

        with torch.no_grad():

            #Get action value
            action_val = self.policy_net(state)
        
        #Train the network
        self.policy_net.train()

        #Eps Greedy action selections
        if rand.rand() > eps:
            return np.argmax(action_val.cpu().data.numpy())
        else:
            return random.choice(np.arange(self.action_size))

    def learn(self, exp):
        state, action, reward, next_state, done = exp

        # Get expected Q values from Policy Model
        Q_expt_current = self.policy_net(state)
        Q_expt = Q_expt_current.gather(1, action.unsqueeze(1)).squeeze(1)

        # Get max predicted Q values for next state from target model
        Q_target_next = self.target_net(next_state).detach().max(1)[0]

        # Compute Q targets for current states
        Q_target = reward + (self.gamma * Q_target_next * (1 - done))

        # Compute Loss
        loss = F.mse_loss(Q_expt, Q_target)

        # Minimize loss
        self.optimiser.zero_grad()
        loss.backward()
        self.optimiser.step()

        self.soft_update(self.policy_net, self.target_net, self.tau)

    def model_dict(self, epsilon)-> dict:
        ''' To save models'''
        return {'policy_net': self.policy_net.state_dict(), 'target_net': self.target_net.state_dict(),
                 't_step': self.t_step, 'epsilon': epsilon}

    def load_model(self, state_dict):
        '''Load Parameters and Model Information from prior training'''
        self.policy_net.load_state_dict(state_dict['policy_net'])
        self.target_net.load_state_dict(state_dict['target_net'])

        #Load the model
        self.policy_net.eval()
        self.target_net.eval()
        self.t_step = state_dict['t_step']

    # θ'=θ×τ+θ'×(1−τ)
    def soft_update(self, policy_model, target_model, tau):
        for t_param, p_param in zip(target_model.parameters(), policy_model.parameters()):
            t_param.data.copy_(tau * p_param.data + (1.0 - tau) * t_param.data)