#!/usr/bin/env python

############################
#-------Orbital 2020-------#
############################
import configparser
from classes.game import GameWindow

def convertType(pair:tuple):
    """Convert items to the appropriate types"""

    #Check if it is boolean
    if pair[1] == "True" or pair[1] == "true":
        return pair[0],True
    elif pair[1] == "False" or pair[1] == "false":
        return pair[0],False

    #Check if it is numbers
    elif pair[1].isdigit():
        return pair[0],int(pair[1])

    #Otherwise return the original pair
    else:
        return pair

def read_settings(config_path:str, key:str) -> dict:
    """Read the configurations of the config file
        Argument:
            config_path: Path of the config file in a string
            key: Get the specific setting based on the key in a string
        Returns:
            Dictionary containing the settings all values are strings
    """

    #Set up the config parser
    config = configparser.ConfigParser()

    #Read the configs
    config.read(config_path)

    #Return the dictionary after converting numbers to int
    return dict(map(lambda x: convertType(x) ,config[key].items()))
    
#Run the following if the file is run as main
if __name__ =="__main__":

    settings = "settings.cfg"

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

    #Get the settings
    settings = read_settings(settings, "Player")

    #Print the config data if debug is on
    if config['debug']:
        for k,v in config.items():
            print(f"{k} : {v}")

    #Create the new game window with the configurations
    game = GameWindow(player_img_paths = player_img_paths, bullet_img_paths = bullet_img_paths, enemy_img_paths = enemy_img_paths, background_img_paths = background_img_paths, p_settings = settings, **config)
    
    #Run the mainloop for the GameWindow
    game.mainloop()