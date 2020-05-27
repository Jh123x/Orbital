#!/usr/bin/env python

############################
#-------Orbital 2020-------#
############################

#Import all functions from the class package
from classes import *
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
    d = load_all(("player_img_paths", "bullet_img_paths", "enemy_img_paths", "background_img_paths", "explosion_img_paths"), 
                    ("Player Sprites", "Bullet Sprites", "Enemy Sprites", "Background", "Explosion Sprites"), 
                    all_cfg, 
                    __file__)

    #DBPath
    db_path = form_abs_path(__file__,'data/test.db')

    #Sound
    sound_path = dict(zip(all_cfg["Sounds"].keys(),list(map(lambda x: form_abs_path(__file__, x), all_cfg["Sounds"].values()))))

    #Get the settings
    settings = all_cfg["Player"]

    #Print the config data if debug is on
    if config['debug']:

        #Print the main config
        for k,v in config.items():
            print(f"{k} : {v}")

    #Create the new game window with the configurations
    game = GameWindow(**d, sound_path = sound_path, p_settings = settings, **config, db_path = db_path)

    #Run the mainloop for the GameWindow
    game.mainloop()

#Run the following if the file is run as main
if __name__ =="__main__":
    main()