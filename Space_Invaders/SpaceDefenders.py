############################
#-------Orbital 2020-------#
############################

#Import functions from the class package
import os
import sys
from classes import GameWindow, list_dir, form_abs_path, read_all

def get_curr_path():
    """Get the path to the current file depending on state of application"""
    #Return correct directory
    return sys.executable if getattr(sys, 'frozen', False) else __file__

def map_dir(*args):
    """Map the abs path for the files in the folder"""
    return list_dir(form_abs_path(get_curr_path(), os.path.join(*args)))

def create_config_file(name:str) -> None:
    """Create a basic config file"""

    #Data in the base config file
    data = """[Space Invaders]
#Do not touch these parameters
sensitivity = 5
maxfps = 60
game_width = 600
game_height = 800

#Debug mode
debug = false

#Path to icon
icon_img_path = images/icon/icon.png

#Path to database (DO NOT TOUCH)
db_path = data/test.db

#Path to store screenshots
screenshot_path = screenshots

[Sounds]
#Path of the different sounds
click = sounds/click.wav
explosion = sounds/Explosion_short.wav
gameover = sounds/Gameover.wav
shooting = sounds/Shooting.wav
exit = sounds/exit.wav
pause = sounds/pause.wav
screenshot = sounds/screenshot.wav
victory = sounds/victory.wav
powerup = sounds/powerup.wav"""

    #If the name contains the .cfg file
    if name[-4:] != ".cfg":
        name += '.cfg'

    #Open the file in write mode
    with open(name, 'w') as file:

        #Write the settings into the file
        file.write(data)

def main() -> None:
    """The main function to run the game"""

    #The path of the configuration file
    settings = "settings.cfg"

    #If the settings file is missing
    if not os.path.isfile(form_abs_path(get_curr_path(),settings)):

        #Create the settings file
        create_config_file(form_abs_path(get_curr_path(),settings))
        
    #Read the configuration file for space invaders
    all_cfg = read_all(form_abs_path(get_curr_path(),settings))
    
    #Main configurations
    config = all_cfg['Space Invaders']
    config['icon_img_path'] = form_abs_path(get_curr_path(), config['icon_img_path'])

    #load soundpath
    config['db_path'] = form_abs_path(get_curr_path(), config['db_path'])

    #load screenshot path
    config['screenshot_path'] = form_abs_path(get_curr_path(), config['screenshot_path'])

    #Load the other sprites
    d = {}
    d["bullet_img_paths"] = map_dir("images", "bullets")
    d["player_img_paths"] = map_dir("images","player")
    d["enemy_img_paths"] = map_dir("images", "enemies")
    d["background_img_paths"] = map_dir("images", "backgrounds")
    d["explosion_img_paths"] = map_dir("images", "explosions")
    d["menu_music_paths"] = map_dir("sounds", "menu_music")
    d["powerup_img_path"] = map_dir("images", "powerups")
    d["mothership_img_path"] = map_dir("images", "bosses", "mothership")
    d["trophy_img_path"] = map_dir("images", "trophys")
    d["scout_img_path"] = map_dir("images", "bosses", "scout")
    d["brute_img_path"] = map_dir("images", "bosses", "brute")
    d["crabs_img_path"] = map_dir("images", "bosses", "crabs")
    d["story_img_path"] = map_dir("images", "story assets")
    d["place_holder_path"] = map_dir("images", "place_holder")

    #Get the number of backgrounds
    bg_limit = len(d["background_img_paths"])

    #Sound
    sound_path = dict(zip(all_cfg["Sounds"].keys(), list(map(lambda x: form_abs_path(get_curr_path(), x), all_cfg["Sounds"].values()))))

    #Print the config data if debug is on
    if config['debug']:

        #Print the main config
        for k,v in config.items():
            print(f"{k} : {v}")

    #Create the new game window with the configurations
    game = GameWindow(**d, sound_path = sound_path, **config, bg_limit = bg_limit)

    #Run the mainloop for the GameWindow
    game.mainloop()


#Run the following if the file is run as main
if __name__ =="__main__":
    main()