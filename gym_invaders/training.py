#Python Modules
import pickle
import os
import time
import warnings
import math
import random
import sys
from collections import deque,namedtuple
# Numeric Computation Module
import numpy as np
import numpy.random as rand
# Neural Network Modules
import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as T
import torch.autograd as autograd
# Image Processing
import cv2
import matplotlib.pyplot as plt
#Gym Environment Dependencies
import gym
from gym import wrappers
# Game Dependencies
import pygame
# In house dependencies
import gym_game
from gym_invaders.ai_invader.agent import DQNAgent
from gym_invaders.ai_invader.model import DQNCNN
from gym_invaders.ai_invader.util import stack_frame,preprocess_frame
np.set_printoptions(threshold=sys.maxsize)

#create a local directory to store pickle files from training
PATH = os.getcwd()+'/obj'
os.makedirs('obj', exist_ok=True)

#Retrieve Training Environment
env = gym.make("Invader-v0")

print("The size of frame is: ", env.observation_space.shape)
print("No. of Actions: ", env.action_space.n)
env.reset()
plt.figure()
plt.imshow(env.reset())
plt.title('Original Frame')
plt.show()

def random_play():
    score = 0
    env.reset()
    while True:
        #env.render()
        action = env.action_space.sample()
        state, reward, done, _ = env.step(action)
        score += reward
        print(done)

        if done:
            env.close()
            print("Your Score at end of game is: ", score)
            break

#random_play()

def frame_preprocess(frame):
    # env.reset()
    plt.figure()
    plt.imshow(preprocess_frame(env.reset(), (0, 0, 0, 0), 84), cmap="gray")
    plt.title('Pre Processed image')
    plt.show()

def stack_frames(frames, state, is_new=False):
    '''
    Function combine of utility functions to preprocess the frames
    '''
    frame = preprocess_frame(state, 84)
    frames = stack_frame(frames,frame, is_new)
    return frames

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Device: ', device)

INPUT_SHAPE = (4, 84, 84)
ACTION_SIZE = env.action_space.n
SEED = 0
GAMMA = 0.99           # discount factor
BUFFER_SIZE = 10000   # replay buffer size
BATCH_SIZE = 64        # Update batch size
LR = 0.0001            # learning rate
TAU = 1e-3             # for soft update of target parameters
UPDATE_EVERY = 1       # how often to update the network
UPDATE_TARGET = 1000  # After which thershold replay to be started
EPS_START = 0.99       # starting value of epsilon
EPS_END = 0.01         # Ending value of epsilon
EPS_DECAY = 100         # Rate by which epsilon to be decayed

agent = DQNAgent(INPUT_SHAPE, ACTION_SIZE, SEED, device, BUFFER_SIZE, BATCH_SIZE, GAMMA, LR, TAU, UPDATE_EVERY, UPDATE_TARGET, DQNCNN)

start_epoch = 0
scores = []
scores_window = deque(maxlen=20)

epsilon_delta = lambda frame_idx: EPS_END + (EPS_START-EPS_END) * math.exp(-1. *frame_idx/EPS_DECAY)

def save_obj(obj, name):
    '''Saves the state dictionary int obj path'''
    print('saving')
    torch.save(obj, "/obj/"+name)

def load_obj(agent, path):
    agent.load_model(torch.load(path))

print('begin training')
def train(n_episodes=1000, load = None):
    """
    n_episodes: maximum number of training episodes
    Saves Model every 100 Epochs
    """
    if load:
        agent.load_model(load)
    #env.render()
    for i_episode in range(start_epoch + 1, n_episodes + 1):
        state = stack_frames(None, env.reset(), True)
        score = 0
        eps = epsilon_delta(i_episode)
        env.render()
        while True:
            action = agent.action(state, eps)
            next_state, reward, done, info = env.step(action)
            if not score:
                print(next_state)
                plt.imshow(next_state,interpolation='none')
                plt.show()
            score += reward
            next_state = stack_frames(state, next_state, False)
            agent.step(state, action, reward, next_state, done)
            state = next_state
            if done:
                break
        scores_window.append(score)  # save most recent score
        scores.append(score)  # save most recent score
        print(f'\rEpisode {i_episode}\tAverage Score: {np.mean(scores_window)}')
        print(i_episode)
        # if i_episode==1:
        #     # Testing code for
        #     #print(agent.model_dict())
        #     save_obj(agent.model_dict(),'sample.pth')
        if i_episode % 100 == 0:
            print('\rEpisode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_window)))
            fig = plt.figure()
            ax = fig.add_subplot(111)
            plt.plot(np.arange(len(scores)), scores)
            plt.ylabel('Score')
            plt.xlabel('Episode #')
            plt.save(fig)
            save_obj(agent.model_dict(), 'model.pth')

    return scores

scores = train(1)
#load_obj(agent,path=PATH+'/model.pth')
def trained_agent(agent):
    '''
    Takes a trained agent and plays a game using the trained agent
    '''
    score = 0
    state = stack_frames(None, env.reset(), True)
    while True:
        env.render()
        action = agent.action(state)
        next_state, reward, done, _ = env.step(action)
        score += reward
        state = stack_frames(state, next_state, False)
        if done:
            print("You Final score is:", score)
            break
    env.close()
###
# To view Trained Agent after a checkpoint
#load_obj(agent, path=PATH+'/model.pth')
#trained_agent(agent)

# To resume training from a previous checkpoint to train for x number of epochs
# model = torch.load(PATH+'/model.pth')
# scores = train(n_episodes = 100, load = model)

# Standard Training:
# Trains Model for 1000 games
# scores = train()
