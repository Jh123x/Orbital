#Unit tests
import pygame
import unittest
import os, sys
#Import the main file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import read_settings
from classes.game import GameWindow
#Keyboard pip module

class Test(unittest.TestCase):
    def setup(self):
        """
        The setup to be run before every test case
        """
        return super().setUp()

    def tearDown(self):
        """
        The teardown to be run after every test case
        """
        return super().tearDown()

