#!/usr/bin/env python
from . import Difficulty_enum

class Difficulty(object):
    def __init__(self,difficulty:int):
        """Constructor for the difficulty class"""

        #Load the enum
        self.difficulty = Difficulty_enum(difficulty)

        #Load the variables
        self.load()

    def load(self) -> None:
        """Load the value and name value for the difficulty"""

        #Load the value
        self.value = self.difficulty.value

        #Load the name
        self.name = self.difficulty.name

    def toggle(self) -> None:
        """Toggles the difficulty"""

        #Check if it is not the max difficulty
        if self.difficulty.value < 5:

            #Set the difficulty to 1 higher
            self.difficulty =  Difficulty_enum(self.difficulty.value + 1)

        #Otherwise
        else:

            #Reset it to 1
            self.difficulty = Difficulty_enum(1)

        #Reload the value and name
        self.load()

    def get_multiplier(self, value:int) -> int:
        """Get multiplier for the current difficulty
            Minimum multiplier: 1
        """

        #Get multiplier
        mul = self.value / 2

        #If multiplier is above 1
        if mul*value > 1:

            #Return the multiplier with the value
            return int(mul*value)

        else:

            #Otherwise return 1
            return 1
        