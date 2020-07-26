import gym
import sys
import numpy as np
import cv2
import logging
import pygame
from gym import spaces
from .AI_game import PyGame_2D
from .classes import *

np.set_printoptions(threshold=sys.maxsize)
logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)

class CustomEnv(PyGame_2D,gym.Env):
    def __init__(self, settings = 'settings.cfg', mode:str = 'play'):
        super(gym.Env,self).__init__()
        super().__init__(settings,mode)
        self.action_space = spaces.Discrete(6)  # Actions are move left, move right, shoot, do nothing, mv left and shoot and move right then shoot
        self.observation_space = spaces.Box(low=0,high=255, shape=(160, 120, 1), dtype=np.uint8)
        self.max_step = 50000
        self.time = 0
        self.display = True
        self.prev_score = 0
        self.prev_life = self.get_player_lives()
        self.prev_enemy = len(self.get_enemies())
        self.action_space = spaces.Discrete(len(self.get_action()))
        
    def reset(self):
        """Reset the environment"""
        self.time = 0
        self.prev_score = 0
        super().reset()
        self.prev_life = self.get_player_lives()
        self.prev_enemy = len(self.get_enemies())
        obs = self.get_space()
        return obs
    
    def calculate_reward(self):
        """Formula for calculating the reward"""
        score = self.get_score() - self.prev_score
        return score - 0.1 + 0.1/2*self.get_player_lives()

    def step(self, action):
        """Each step of the game"""
        self.screen.fill((0, 0, 0))  # fills the entire screen
        self.handle()
        self.action(action)

        if self.display:
            pygame.display.update()

        obs = self.get_space()# observations for the next timestep
        self.time += 1
        
        #Get reward
        reward = self.calculate_reward()
        score = self.get_score() - self.prev_score

        #Update vars
        self.prev_enemy = len(self.get_enemies())
        self.prev_score = self.get_score()
        self.prev_life = self.get_player_lives()

        done = self.is_over()
        debug = {'score': score, 'timestep': self.time, 'reward': reward}
        logging.debug(debug)
        logging.debug(obs.shape)
        logging.debug(self.get_player())
        logging.debug(self.get_enemies())

        return obs, reward, done, debug

    def render(self, state:bool):
        '''Toggle Display Mode of agent'''
        self.display = state

