import gym
import gym_game
import pygame
import numpy as np
import torch
import torch.nn as nn
import random
env = gym.make("Invader-v0")
def simulate(env):
    sum_reward = 0
    for i in range(2):
        state = env.reset()
        for j in range(10000):
            act = env.action_space.sample()
            next_state, reward, done, _ = env.step(act)
            #print(next_state)
            sum_reward +=1
            print(sum_reward)
            state = next_state
            if done == True:
                break
        sum_reward = 0
        env.reset()



if __name__ == "__main__":
    env = gym.make("Invader-v0")
    simulate(env)