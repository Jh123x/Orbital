import os
import pygame
from classes import *

#Test the video playback
pygame.init()

width = 600
height = 800

#Create the pygame display
screen = pygame.display.set_mode((width,height))

#Create video cutscene obj
cutscene = VideoCutscene(width, height, screen, None, os.path.join(os.path.dirname(__file__), "videos", "test.mp4"))

cutscene.play()
