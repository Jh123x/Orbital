#!/usr/bin/env python

############################
#-------Orbital 2020-------#
############################

#Import functions from the class package
from classes import *
import time
import os

def main() -> None:
    """The main function"""
    #DBPath
    db_path = form_abs_path(__file__,'data/test.db')

    #Load the settings database
    settings = SettingsDB(db_path)

    #Convert to correct types
    settings = list(map(lambda x: convertType((x[1].lower(),x[2])),settings.fetch_all()))
    
    #Form paths to become abs paths
    d = {}
    for k,v in settings:
        if type(v) != str:
            d[k] = v
        elif ',' in v:
            d[k] = [os.path.join(os.path.dirname(__file__), x.strip()) for x in v.split(',')]
        elif '_img_paths' in k:
            d[k] = list_dir(os.path.join(os.path.dirname(__file__), v.strip()))

    #Load the other sprites 
    # d["player_img_paths"] = list_dir(form_abs_path(__file__, "images/player"))
    # d["enemy_img_paths"] = list_dir(form_abs_path(__file__, "images/enemies"))
    # d["background_img_paths"] = list_dir(form_abs_path(__file__, "images/backgrounds"))
    # d["explosion_img_paths"] = list_dir(form_abs_path(__file__, "images/explosions"))

    # print(d)
    #Get the number of backgrounds
    bg_limit = len(d["background_img_paths"])

    #Sound
    sound_path = dict(map(lambda x: (os.path.basename(x)[:-4].lower(), x), d['sound']))

    # #Get the settings
    # settings = all_cfg["Player"]

    # #Print the config data if debug is on
    # if config['debug']:

    #     #Print the main config
    #     for k,v in config.items():
    #         print(f"{k} : {v}")

    #Create the new game window with the configurations
    # game = GameWindow(**d, sound_path = sound_path, p_settings = settings, **config, db_path = db_path, bg_limit = bg_limit)

    # #Run the mainloop for the GameWindow
    # game.mainloop()

#Run the following if the file is run as main
if __name__ =="__main__":
    main()