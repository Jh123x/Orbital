import gym
import numpy as np
import torch
import matplotlib.pyplot as plt
import os
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import copy
import gym
import multiprocessing as mp
from joblib import Parallel, delayed, parallel_backend

# In house dependencies
import gym_game
from ai_invader.agent import EvoAgentTrainer
from ai_invader.agent import EvoAgent
from ai_invader.util import load_obj

def make_env():
    envir = gym.make("Classic-v0")
    return envir

#Select device to be used
device = 'cuda' if torch.cuda.is_available() else 'cpu'

#Get the game_actions from the env
action_space = 6

#Get the number of agents per generation
num_agents = 2

#Get the input shape (No of frames, x pixels, y pixels)
#No of frames is to let AI to perceive motion
input_shape = (4, 160, 120)

#Get the Top k scores
elites = 1

#Number of generations to train the AI
generations = 2

#Start evolution
# ag = EvoAgentTrainer(input_shape,action_space, num_agents, elites, 1, env = make_env)
# ag.train(generations)
ag = EvoAgent()
ag.load_model(load_obj('/Users/stephen/GitRepositories/Orbital/gym_invaders/model/abc.pth', device))
print(ag.model)