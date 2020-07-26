import random
import os
from math import exp
import torch
import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt
from .training_agent import TrainingAgent
from .. import ReplayMemory, get_filename
from torch.optim.rmsprop import RMSprop

class DQNAgent(TrainingAgent):
    def __init__(self, input_shape, action_space, seed, device, model, gamma,
                 alpha, tau, batch_size,update, replay, buffer_size, env,
                 decay = 200, path = 'model',num_epochs= 0, max_step = 50000, learn_interval = 20):

        '''Initialise a DQNAgent Object
        buffer_size : size of replay buffer to sample from
        gamma       : discount rate
        alpha       : learn rate
        replay.     : after which replay buffer loading to be started
        update      : update interval of model parameters every x instances of back propagation
        replay.     : after which replay buffer loading to be started
        learn_interval: tick for learning rate
        '''
        super(DQNAgent,self).__init__( input_shape ,action_space ,seed ,device,model,
                                        gamma, alpha, tau, batch_size, max_step, env,num_epochs ,path)
        self.buffer_size = buffer_size
        self.update = update
        self.replay = replay
        self.interval = learn_interval
        # Q-Network
        self.policy_net = self.model(input_shape, action_space).to(self.device)
        self.target_net = self.model(input_shape, action_space).to(self.device)
        self.optimiser = RMSprop(self.policy_net.parameters(), lr=self.alpha)
        # Replay Memory
        self.memory = ReplayMemory(self.buffer_size, self.batch_size, self.seed, self.device)
        # Timestep
        self.t_step = 0
        self.l_step = 0

        self.EPSILON_START = 1.0
        self.EPSILON_FINAL = 0.02
        self.EPS_DECAY = decay
        self.epsilon_delta = lambda frame_idx: self.EPSILON_FINAL + (self.EPSILON_START - self.EPSILON_FINAL) * exp(-1. * frame_idx / self.EPS_DECAY)

    def step(self, state, action, reward, next_state, done):
        '''
        Step of learning and taking environment action.
        '''

        # Save experience into replay buffer
        self.memory.add(state, action, reward, next_state, done)

        # Learn every update % timestep
        self.t_step = (self.t_step + 1) % self.interval

        if self.t_step == 0:
            # if there are enough samples in the memory, get a random subset and learn
            if len(self.memory) > self.replay:
                experience = self.memory.sample()
                print('learning')
                self.learn(experience)


    def action(self, state, eps=0.):
        ''' Returns action for given state as per current policy'''
        #Unpack the state
        state = torch.from_numpy(state).unsqueeze(0).to(self.device)
        if rand.rand() > eps:
            # Eps Greedy action selections
            action_val = self.policy_net(state)
            return np.argmax(action_val.cpu().data.numpy())
        else:
            return random.choice(np.arange(self.action_space))

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
        loss = torch.nn.functional.mse_loss(Q_expt, Q_target)

        # Minimize loss
        self.optimiser.zero_grad()
        loss.backward()
        self.optimiser.step()
        self.l_step = (self.l_step +1) % self.update
        if self.t_step == 0:
            self.soft_update(self.policy_net, self.target_net, self.tau)

    def model_dict(self)-> dict:
        ''' To save models'''
        return {'policy_net': self.policy_net.state_dict(), 'target_net': self.target_net.state_dict(),
                'optimizer': self.optimiser.state_dict(), 'num_epoch': self.num_epochs,'scores': self.scores}

    def load_model(self, state_dict,eval = True):
        '''Load Parameters and Model Information from prior training for continuation of training'''
        self.policy_net.load_state_dict(state_dict['policy_net'])
        self.target_net.load_state_dict(state_dict['target_net'])
        self.optimiser.load_state_dict(state_dict['optimizer'])
        self.scores = state_dict['scores']
        if eval:
            self.policy_net.eval()
            self.target_net.eval()
        else:
            self.policy_net.train()
            self.target_net.train()
        #Load the model
        self.num_epochs = state_dict['num_epoch']

    # θ'=θ×τ+θ'×(1−τ)
    def soft_update(self, policy_model, target_model, tau):
        for t_param, p_param in zip(target_model.parameters(), policy_model.parameters()):
            t_param.data.copy_(tau * p_param.data + (1.0 - tau) * t_param.data)

    def train(self, n_episodes=1000):
        """
        n_episodes: maximum number of training episodes
        Saves Model every 100 Epochs
        """
        filename = get_filename()


        # Toggles the render on
        for i_episode in range(n_episodes):
            self.num_epochs += 1
            state = self.stack_frames(None, self.reset(), True)
            score = 0
            eps = self.epsilon_delta(self.num_epochs)
            self.save_obj(self.model_dict(), os.path.join(self.path, filename))
            while True:
                action = self.action(state, eps)

                next_state, reward, done, info = self.env.step(action)

                score += reward

                next_state = self.stack_frames(state, next_state, False)

                self.step(state, action, reward, next_state, done)
                state = next_state
                if done:
                    break
            self.scores.append(score)  # save most recent score

            # Every 100 training
            if i_episode % 100 == 0:
                self.save_obj(self.model_dict(), os.path.join(self.path, filename))
                print(f"Creating plot")
                # Plot a figure
                fig = plt.figure()

                # Add a subplot
                # ax = fig.add_subplot(111)

                # Plot the graph
                plt.plot(np.arange(len(self.scores)), self.scores)

                # Add labels
                plt.xlabel('Episode #')
                plt.ylabel('Score')

                # Save the plot
                plt.savefig(f'{i_episode} plot.png')
                print(f"Plot saved")

        # Return the scores.
        return self.scores

    def eval(self):
        score = 0
        state = self.stack_frames(None, self.reset(), True)
        # Render gym environment
        self.env.render(True)
        while True:

            action = self.action(state)
            next_state, reward, done, _ = self.env.step(action)
            score += reward
            state = self.stack_frames(state, next_state, False)
            if done:
                print("You Final score is:", score)
                break

