import gym
import sys
import pygame
from gym import spaces
import numpy as np
import logging
from .classes import *
from .custom_env import CustomEnv

np.set_printoptions(threshold=sys.maxsize)
logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)

class ClassicEnv(CustomEnv):
    def __init__(self, settings = "settings.cfg"):
        super().__init__(settings,'classic')

    def create_screen(self):
        """Create the classic screen"""
        return ClassicScreen(self.screen_width, self.screen_height, self.screen, 5, self.fps, Difficulty(4))