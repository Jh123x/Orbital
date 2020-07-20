############################
#-------Orbital 2020-------#
############################

#Import functions from the class package

from classes import GameWindow, list_dir, form_abs_path, read_all, load_all
import sys
import os

def get_curr_path():
    """Get the path to the current file depending on state of application"""
    #Return correct directory
    return sys.executable if getattr(sys, 'frozen', False) else __file__

def map_dir(*args):
    """Map the abs path for the files in the folder"""
    return list_dir(form_abs_path(get_curr_path(), os.path.join(*args)))

def main() -> None:
    """The main function to run the game"""

    #The path of the configuration file
    settings = "settings.cfg"

    #Read the configuration file for space invaders
    all_cfg = read_all(form_abs_path(get_curr_path(),settings))
    
    #Main configurations
    config = all_cfg['Space Invaders']
    config['icon_img_path'] = form_abs_path(get_curr_path(), config['icon_img_path'])

    #Load all
    d = load_all(("bullet_img_paths",), ("Bullet Sprites",), all_cfg, get_curr_path())

    #load soundpath
    config['db_path'] = form_abs_path(get_curr_path(), config['db_path'])

    #Load the other sprites
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

    #AI Configs
    ai_config = all_cfg['AI']
    d['ai_model_path'] = form_abs_path(get_curr_path(), ai_config["model_path"])
    d['ai_input_shape'] = tuple(map(int, ai_config["input_shape"].split(',')))

    #Get the number of backgrounds
    bg_limit = len(d["background_img_paths"])

    #Sound
    sound_path = dict(zip(all_cfg["Sounds"].keys(),list(map(lambda x: form_abs_path(get_curr_path(), x), all_cfg["Sounds"].values()))))

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