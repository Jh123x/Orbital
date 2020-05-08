############################
#-------Orbital 2020-------#
############################
import configparser
from classes.game import GameWindow

def read_settings(config_path:str, key:str) -> dict:
    """Read the configurations of the config file
        Argument:
            config_path: Path of the config file in a string
            key: Get the specific setting based on the key in a string
        Returns:
            Dictionary containing the settings all values are strings
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    return dict(map(lambda x: (x[0],int(x[1])),config[key].items()))
    
#Run the following if the file is run as main
if __name__ =="__main__":

    #Read the configuration file for space invaders
    config = read_settings("settings.cfg","Space Invaders")
    print(config)


    
