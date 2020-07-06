import gym
import sys
import numpy as np
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
        self.observation_space = spaces.Box(0, 1, shape=(800, 600, 1), dtype=np.bool_)
        self.max_step = 50000
        self.time = 0
        self.display = False
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

        obs = self.get_space()  # observations for the next timestep
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



# class CustomEnv(gym.Env):
#     #metadata = {'render.modes' : ['human']}
#     def __init__(self):
#         self.settings = "settings.cfg"
#         self.pygame = PyGame_2D(self.settings)
#         self.action_space = spaces.Discrete(6)# Actions are move left, move right, shoot, do nothing, mv left and shoot and move right then shoot
#         self.observation_space = spaces.Box(0,1,shape=(800,600,1),dtype = np.bool_)
#         self.time = 0
#         self.max_step = 50000
#         self.score = 0
#         self.display = False

#     def reset(self):
#         del self.pygame
#         self.pygame = PyGame_2D(self.settings)
#         obs = self.pygame.get_space()
#         self.time = 0
#         self.score = 0
#         return obs

#     def step(self, action):
#         self.pygame.screen.fill((0,0,0)) #fills the entire screen
#         self.pygame.handle()
#         self.pygame.action(action)
#         #self.pygame.state.draw_hitboxes()
#         if self.display:
#             pygame.display.update()
#         obs = self.pygame.get_space() # observations for the next timestep
#         #print(obs)
#         self.time += 1
#         score = self.pygame.get_score() - self.score
#         self.score = self.pygame.get_score()
#         # Reward is a combination of current score*(time/max_time) + Penalty of timestep
#         reward = score

#         done = self.pygame.is_over()
#         debug = {'score': score, 'timestep': self.time, 'reward': reward}

#         #print(obs.shape)
#         #print(self.pygame.get_player())
#         #print(self.pygame.get_enemies())

#         return obs, reward, done, debug

#     def start(self):
#         #pygame.display.update = function_combine(pygame.display.update,self.on_screen_update())
#         #self.pygame.mainloop()
#         pass
#     def render(self, mode="human", close=False):
#         #self.pygame.mainloop()
#         self.display = not self.display
