#!/usr/bin/env python

############################
#-------Orbital 2020-------#
############################

#Import functions from the class package
from classes import GameWindow, list_dir, form_abs_path, read_all, load_all
import time

def main() -> None:
    """The main function"""

    #The path of the configuration file
    settings = "settings.cfg"

    #Read the configuration file for space invaders
    all_cfg = read_all(form_abs_path(__file__,settings))
    
    #Main configurations
    config = all_cfg['Space Invaders']
    config['icon_img_path'] = form_abs_path(__file__, config['icon_img_path'])

    #Load all
    d = load_all(("bullet_img_paths",), ("Bullet Sprites",), all_cfg, __file__)

    #Load the other sprites 
    d["player_img_paths"] = list_dir(form_abs_path(__file__, "images/player"))
    d["enemy_img_paths"] = list_dir(form_abs_path(__file__, "images/enemies"))
    d["background_img_paths"] = list_dir(form_abs_path(__file__, "images/backgrounds"))
    d["explosion_img_paths"] = list_dir(form_abs_path(__file__, "images/explosions"))

    #Get the number of backgrounds
    bg_limit = len(d["background_img_paths"])
    
    #DBPath
    db_path = form_abs_path(__file__,'data/test.db')

    #Sound
    sound_path = dict(zip(all_cfg["Sounds"].keys(),list(map(lambda x: form_abs_path(__file__, x), all_cfg["Sounds"].values()))))

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