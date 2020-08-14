############################
#-------Orbital 2020-------#
############################

#Import other dependencies
import os
import sys

#Initialise pygame
import pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

#Functions from the class package
from classes import GameWindow, list_dir, form_abs_path, read_all, create_config_file

def main() -> None:
    """The main function to run the game"""

    #Run the game
    run_game(load_settings("settings.cfg"))

def load_settings(settings_path:str) -> dict:
    """Load settings value of the game"""

    #If the settings file is missing
    if not os.path.isfile(form_abs_path(get_curr_path(),settings_path)):

        #Create the settings file
        create_config_file(form_abs_path(get_curr_path(),settings_path))
        
    #Read the configuration file for space invaders
    all_cfg = read_all(form_abs_path(get_curr_path(),settings_path))
    
    #Main configurations
    config = all_cfg['Space Invaders']
    config['icon_img_path'] = form_abs_path(get_curr_path(), config['icon_img_path'])

    #load soundpath
    config['db_path'] = form_abs_path(get_curr_path(), config['db_path'])

    #load screenshot path
    config['screenshot_path'] = form_abs_path(get_curr_path(), config['screenshot_path'])

    #Load the other sprites
    config["mothership_img_path"]  = map_dir("images", "bosses", "mothership")
    config["background_img_paths"] = map_dir("images", "backgrounds")
    config["explosion_img_paths"]  = map_dir("images", "explosions")
    config["place_holder_path"]    = map_dir("images", "place_holder")
    config["pointer_img_path"]     = map_dir("images", "pointer")
    config["bullet_img_paths"]     = map_dir("images", "bullets")
    config["player_img_paths"]     = map_dir("images","player")
    config["menu_music_paths"]     = map_dir("sounds", "menu_music")
    config["powerup_img_path"]     = map_dir("images", "powerups")
    config["enemy_img_paths"]      = map_dir("images", "enemies")
    config["trophy_img_path"]      = map_dir("images", "trophys")
    config["scout_img_path"]       = map_dir("images", "bosses", "scout")
    config["brute_img_path"]       = map_dir("images", "bosses", "brute")
    config["crabs_img_path"]       = map_dir("images", "bosses", "crabs")
    config["story_img_path"]       = map_dir("images", "story assets")

    #Get the number of backgrounds
    config['bg_limit'] = len(config["background_img_paths"])

    #Sound
    config['sound_path'] = dict(zip(all_cfg["Sounds"].keys(), list(map(lambda x: form_abs_path(get_curr_path(), x), all_cfg["Sounds"].values()))))

    #Return the dict
    return config

def run_game(config:dict):
    """Run the game"""

    #Create the new game window with the configurations
    game = GameWindow(**config)

    #Run the mainloop for the GameWindow
    game.mainloop()

def get_curr_path():
    """Get the path to the current file depending on state of application"""
    #Return correct directory
    return sys.executable if getattr(sys, 'frozen', False) else __file__

def map_dir(*args):
    """Map the abs path for the files in the folder"""
    return list_dir(form_abs_path(get_curr_path(), os.path.join(*args)))


#Run the following if the file is run as main
if __name__ =="__main__":
    main()