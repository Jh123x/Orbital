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
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
from stable_baselines3.ppo import CnnPolicy
env = gym.make("Invader-v0")
check_env(env)
def random_play():
    score = 0
    env.reset()
    done = False
    while not done:
        #env.render()
        action = env.action_space.sample()
        state, reward, done, _ = env.step(action)
        score += reward
        #print(reward)

    env.close()
    print("Your Score at end of game is: ", score)


if __name__ == "__main__":
    env = gym.make("Invader-v0")
    random_play()
    model = PPO(CnnPolicy, env,n_steps=5000,batch_size=64, n_epochs= 10, gamma=0.99, gae_lambda=0.95, clip_range=0.2,
                ent_coef=0.0,vf_coef=0.5,max_grad_norm=0.5 ,verbose=2, tensorboard_log='./')
    # model.learn(total_timesteps=50000)
    # model.save("ppo_classic")
    model = PPO.load("ppo_classic")

    obs = env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render(True)
