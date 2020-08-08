import asyncio
import pygame
import os
from . import Sound

def load_sprites(obj_list:list, paths:list):
    """Load the sprites for each of the items in parallel"""

    #Run functions concurrently
    for i, obj in enumerate(obj_list):

        #Add image sprites to each class concurrently
        asyncio.run(add_to_sprite(obj, paths[i]))

def load_pointers(obj_list:tuple, screen):
    """Load the pointer for the screen"""
    for obj in obj_list:
        screen.pointers.append(pygame.image.load(obj))

def load_sprites_dict(obj_list:list, paths:list) -> None:
    """Load the sprites as dict"""
    #Run functions concurrently
    for i, obj in enumerate(obj_list):

        #Add image sprites to each class concurrently
        asyncio.run(add_to_sprite_dict(obj, paths[i]))

def load_img(path:str):
    """Load image"""
    return pygame.image.load(path)

async def add_to_sprite(obj, sprite_path:list) -> None:
    """Add the pygame image to the object"""
    #For each object load the image and append it to the object
    for path in sprite_path:

        #Append the sprite
        obj.sprites.append(load_img(path))

async def add_to_sprite_dict(obj, sprite_path:list) -> None:
    """Add the pygame image to the object"""
    #For each object load the image and append it to the object
    for path in sprite_path:

        #Added the name to the sprite dict
        obj.sprites_dict[os.path.basename(path)[:-4]] = load_img(path)
        
async def load_sound(sound_path:str, settings:int, volume:float, debug:bool) -> Sound:
    """Load the sound object"""
    return Sound(dict(map(lambda x: (x[0], pygame.mixer.Sound(x[1])), sound_path.items())), bool(int(settings)), volume, debug)