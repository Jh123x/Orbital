import gym
import sys
from gym import spaces
import numpy as np
from .Classic import PyGameClassic
from .classes import *
np.set_printoptions(threshold=sys.maxsize)

class ClassicEnv(gym.Env):
    def __init__(self):
        self.settings = "settings.cfg"
        self.pygame = PyGameClassic(self.settings)
        self.action_space = spaces.Discrete(
            6)  # Actions are move left, move right, shoot, do nothing, mv left and shoot and move right then shoot
        self.observation_space = spaces.Box(0, 1, shape=(800, 600, 1), dtype=np.bool_)
        self.time = 0
        self.max_step = 50000
        self.score = 0

    def reset(self):
        del self.pygame
        self.pygame = PyGameClassic(self.settings)
        obs = self.pygame.get_space()
        self.time = 0
        self.score = 0
        return obs

    def step(self, action):
        self.pygame.screen.fill((0, 0, 0))  # fills the entire screen
        self.pygame.state.handle()
        self.pygame.action(action)
        pygame.display.update()
        obs = self.pygame.get_space_boolean()  # observations for the next timestep
        self.time += 1
        score = self.pygame.get_score() - self.score
        self.score = self.pygame.get_score()
        # Reward is a combination of current score*(time/max_time) + Penalty of timestep
        reward = score

        done = self.pygame.is_over()
        debug = {'score': score, 'timestep': self.time, 'reward': reward}

        # print(obs.shape)
        # print(self.pygame.get_player())
        # print(self.pygame.get_enemies())

        return obs, reward, done, debug

    def on_screen_update(self):
        """"""
        print("hello from listener")
        # print(self.pygame.get_space().shape)

    def start(self):
        # pygame.display.update = function_combine(pygame.display.update,self.on_screen_update())
        # self.pygame.mainloop()
        pass

    def render(self, mode="human", close=False):
        # self.pygame.mainloop()
        pass
