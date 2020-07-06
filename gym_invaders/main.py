import gym
import gym_game
from gym import wrappers
import pygame
# from skimage import transform
from collections import deque,namedtuple
import matplotlib.pyplot as plt
import time
import warnings
import math
import random
import numpy as np
import numpy.random as rand
import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as T
import torch.autograd as autograd
import cv2
import ai_invader
env = gym.make("Invader-v0")

def random_play():
    score = 0
    env.reset()
    done = False
    while not done:
        #env.render()
        action = env.action_space.sample()
        state, reward, done, _ = env.step(action)
        score += reward
        print(reward)

    env.close()
    print("Your Score at end of game is: ", score)


if __name__ == "__main__":
    env = gym.make("Invader-v0")
    random_play()
