#Import the everything from the game folder
from Game import *
from Misc import *
#Code for the AI of the bot
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

#Creating random tensor
x = torch.rand(5, 3)
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
playgame()

