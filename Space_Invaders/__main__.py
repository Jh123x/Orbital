############################
#-------Orbital 2020-------#
############################

#Import functions from the class package
from classes import GameWindow, list_dir, form_abs_path, read_all, load_all
import sys
import os

def get_curr_path():
    """Get the path to the current file
        Doesn't use __file__ directly as it does not work then the executable is frozen
    """
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = sys.executable
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = __file__
    return datadir

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

    #Load the other sprites
    d["player_img_paths"] = list_dir(form_abs_path(get_curr_path(), os.path.join("images","player")))
    d["enemy_img_paths"] = list_dir(form_abs_path(get_curr_path(), os.path.join("images", "enemies")))
    d["background_img_paths"] = list_dir(form_abs_path(get_curr_path(), os.path.join("images", "backgrounds")))
    d["explosion_img_paths"] = list_dir(form_abs_path(get_curr_path(), os.path.join("images", "explosions")))
    d["menu_music_paths"] = list_dir(form_abs_path(get_curr_path(), os.path.join("sounds", "menu_music")))
    d["powerup_img_path"] = list_dir(form_abs_path(get_curr_path(), os.path.join("images", "powerups")))
    d["mothership_img_path"] = list_dir(form_abs_path(get_curr_path(), os.path.join("images", "bosses", "mothership")))
    d["trophy_img_path"] = list_dir(form_abs_path(get_curr_path(), os.path.join("images", "trophys")))

    #Get the number of backgrounds
    bg_limit = len(d["background_img_paths"])
    
    #DBPath
    db_path = form_abs_path(get_curr_path(),'data/test.db')

    #Sound
    sound_path = dict(zip(all_cfg["Sounds"].keys(),list(map(lambda x: form_abs_path(get_curr_path(), x), all_cfg["Sounds"].values()))))

    #Print the config data if debug is on
    if config['debug']:

        #Print the main config
        for k,v in config.items():
            print(f"{k} : {v}")

    #Create the new game window with the configurations
    game = GameWindow(**d, sound_path = sound_path, **config, db_path = db_path, bg_limit = bg_limit)

    #Run the mainloop for the GameWindow
    game.mainloop()

#Run the following if the file is run as main
if __name__ =="__main__":
    main()