#!/usr/bin/env python

############################
#-------Orbital 2020-------#
############################

#Import all functions from the class package
from classes import *
import os

def form_abs_path(filepath):
    """Get the absolute path of a filepath"""
    return f"{os.path.dirname(os.path.realpath(__file__))}/{filepath}"
    
#Run the following if the file is run as main
if __name__ =="__main__":

    #The path of the configuration file
    settings = "settings.cfg"

    #Read the configuration file for space invaders
    all_cfg = read_all(form_abs_path(settings))
    
    #Main configurations
    config = all_cfg['Space Invaders']
    config['icon_img_path'] = form_abs_path(config['icon_img_path'])

    #Get the player sprites
    player_img_paths = list(map(lambda x: form_abs_path(x), all_cfg["Player Sprites"].values()))

    #Get the bullet sprites Enemy Sprites
    bullet_img_paths = list(map(lambda x: form_abs_path(x), all_cfg["Bullet Sprites"].values()))

    #Get the enemy sprites
    enemy_img_paths = list(map(lambda x: form_abs_path(x), all_cfg["Enemy Sprites"].values()))

    #Get the background sprites
    background_img_paths = list(map(lambda x: form_abs_path(x), all_cfg["Background"].values()))

    #Get the explosion image path
    explosion_img_paths = list(map(lambda x: form_abs_path(x), all_cfg["Explosion Sprites"].values()))

    #DBPath
    db_path = form_abs_path('data/test.db')

    #Get the settings
    settings = all_cfg["Player"]

    #Print the config data if debug is on
    if config['debug']:

        #Print the main config
        for k,v in config.items():
            print(f"{k} : {v}")

    #Create the new game window with the configurations
    game = GameWindow(player_img_paths = player_img_paths, bullet_img_paths = bullet_img_paths, enemy_img_paths = enemy_img_paths, explosion_img_paths = explosion_img_paths, background_img_paths = background_img_paths, p_settings = settings, **config, db_path = db_path)
    
    #Run the mainloop for the GameWindow
    game.mainloop()