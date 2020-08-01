#To read the configuration files
import configparser
import os

def list_dir(filepath):
    """List the files in the directory"""
    return sorted(list(map(lambda x: os.path.join(filepath,x),os.listdir(filepath))))

def form_abs_path(current_path:str, filepath:str):
    """Get the absolute path of a filepath"""
    return os.path.join(os.path.dirname(current_path),filepath)

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


def convertType(pair:tuple):
    """Convert items to the appropriate types
        Arguments:
            pair: A tuple containing 2 items
        Returns:
            pair: A tuple containing 2 items where the second item is converted to the appropriate types
    """

    #If it is not a pair
    if len(pair) != 2:

        #Return the pair
        return pair

    #Check if it is boolean
    if pair[1].lower() == "true":
        return pair[0],True
    elif pair[1].lower() == "false":
        return pair[0],False

    #Check if it is numbers
    elif pair[1].isdigit():
        if pair[0].isdigit():
            return int(pair[0]), int(pair[1])
        else:
            return pair[0],int(pair[1])

    #Otherwise return the original pair
    else:
        return pair

def read_all(config_path:str) -> dict:
    """Read all the configurations from the config file
        Arguments: 
            config_path: path to the config file
        returns: 
            A dictionary with each of the keywords matched to the keys
    """
    #Set up the config parser
    config = configparser.ConfigParser()

    #Read the configs
    config.read(config_path)

    #Return all of the configs as a dictionary
    return dict(map(lambda x: (x[0],dict(map(lambda x: convertType(x),x[1].items()))), config.items()))

def main() -> None:
    """The main function for this file"""
    print(read_all('../../settings.cfg'))

if __name__ == '__main__':
    main()