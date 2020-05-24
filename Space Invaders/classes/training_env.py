"""from __future__ import print_function
import gym
from Game import *
from Misc import *
from gym import spaces
import numpy as np
import pygame
import pygame.freetype
import pygame.time
from pygame.locals import *

class SpaceDefendersEnv(gym.Env):
    """ 
    Custom environment for Space Defenders following gym interface
    """
    metadata = {'render.modes':['human']}
    def __init__(self, gamewindow,player, max_step, ):
        super(SpaceDefendersEnv,self).__init__()
        pygame.init()
        self.game = gamewindow
        #define action and observation space
        self.player = player
        # The actions in this action space -> {Move left, Move right, Shoot}
        self.action_space = spaces.Discrete(3)
        
        # Gym environment of the observation space, taking whole screen RGB values as well as number of lives
        self.observation_space = gym.spaces.Box(low = 0,high = 1, dtype = np.uint8,shape=(600,800))
        self.timestep = 0
        self.max_step = max_step
        self.seed()
        self.time = pygame.time.Clock()
        self.prev_action = -1 # initialisation

    def step(self, action):
        """ 
        Run one time step of the environment dynamics, when end of episode is reached.
        call reset to reset the environment's state

        Arguments:
            action {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        if self.game.get_state() != State.PLAY:
            return self.reset()
        self.player
        self.timestep = self.time.get_time()
        observation = self.game.get_screen
        time_mod = self.timestep/self.max_step
        reward = self.game.get_score() * time_mod
        obs = pygame
        return obs, reward, self.game.get_state()==State.PLAY, {'reward': reward, 'time_mod' : time_mod , 'time step to seconds' : self.timestep/60}
    
    def _take_action(self,action)

    def reset(self):
        self.game.


def playgame():
    #The path of the configuration file
    settings = "../settings.cfg"

    #Read the configuration file for space invaders
    config = read_settings(settings,"Space Invaders")

    #Get the player sprites
    player_img_paths = tuple(read_settings(settings, "Player Sprites").values())

    #Get the bullet sprites Enemy Sprites
    bullet_img_paths = tuple(read_settings(settings, "Bullet Sprites").values())

    #Get the enemy sprites
    enemy_img_paths = tuple(read_settings(settings, "Enemy Sprites").values())

    #Get the background sprites
    background_img_paths = tuple(read_settings(settings, "Background").values())

    #Get the explosion image path
    explosion_img_paths = tuple(read_settings(settings, "Explosion Sprites").values())

    #Get the settings
    settings = read_settings(settings, "Player")
    game = GameWindow(player_img_paths = player_img_paths, bullet_img_paths = bullet_img_paths, enemy_img_paths = enemy_img_paths, explosion_img_paths = explosion_img_paths, background_img_paths = background_img_paths, p_settings = settings, **config)
    
    #Run the mainloop for the GameWindow
    game.mainloop()
playgame()"""