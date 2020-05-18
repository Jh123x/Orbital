#Code for the AI of the bot
from __future__ import print_function
import torch
import numpy as np
import pygame
import pygame.surfarray
from pygame.constants import K_DOWN, KEYDOWN,KEYUP,K_UP,QUIT

def function_combine(screen_update, intercept_func):  
    """
    Wrapper function to intercept screen of the game
    """
   def wrap(*args, **kwargs):  
     screen_update(*args, **kwargs) # call the screen update func we intercepted so the screen buffer is updated  
     intercept_func() # call our own function to get the screen buffer  
   return wrap

def on_screen_update():
   """
   Tester Function to get screen
   """
   surface_array = pygame.surfarray.array3d(pygame.display.get_surface())
   print("We got the screen array")
   print(surface_array)

 def function_intercept(intercepted_func, intercepting_func):  
   def wrap(*args, **kwargs):  
     # call the function we are intercepting and get it's result  
     real_results = intercepted_func(*args, **kwargs)
     # call our own function and return our new results  
     new_results = intercepting_func(real_results, *args, **kwargs)  
     return new_results  
   return wrap  

 def just_press_down_key(actual_events, *args, **kwargs):
   return [pygame.event.Event(KEYDOWN, {"key": K_DOWN})]

 # set our on_screen_update function to always get called whenever the screen updated
pygame.display.update = function_combine(pygame.display.update, on_screen_update)
 # FYI the screen can also be modified via flip, so this might be needed for some games
pygame.display.flip = function_combine(pygame.display.flip, on_screen_update)
