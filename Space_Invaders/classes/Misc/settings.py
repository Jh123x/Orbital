#To read the configuration files
import configparser
import os

def list_dir(filepath):
    """List the files in the directory"""
    return tuple(map(lambda x: "/".join((filepath,x)),os.listdir(filepath)))

def num_files(filepath):
    """Find the number of files in the directory"""
    return len(list_dir(filepath))

def load_all(kv:tuple, keys:tuple, dic:dict, curr_path:str):
    """Load all the sprites"""
    #Create dict
    d = {}

    #Add the function to list of tasks
    for i,key in enumerate(keys):
        map_abs_path(kv[i],dic[key].values(),d,curr_path)

    #Return the dictionary
    return d

def map_abs_path(key:str, paths:list, dic:dict, curr_path:str):
    """Map absolute path"""
    dic[key] = list(map(lambda x: form_abs_path(curr_path, x), paths))

def form_abs_path(current_path:str, filepath:str):
    """Get the absolute path of a filepath"""
    return f"{os.path.dirname(os.path.realpath(current_path))}/{filepath}"

def convertType(pair:tuple):
    """Convert items to the appropriate types
        Arguments:
            pair: A tuple containing 2 items
        Returns:
            pair: A tuple containing 2 items where the second item is converted to the appropriate types
    """

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