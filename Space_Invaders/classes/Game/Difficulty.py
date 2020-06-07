from . import Difficulty_enum

class Difficulty(object):
    def __init__(self,difficulty:int):
        """Initialize the class"""
        self.difficulty = Difficulty_enum(difficulty)
        self.load()

    def load(self):
        self.value = self.difficulty.value
        self.name = self.difficulty.name

    def toggle(self) -> None:
        """Get the toggle"""
        if self.difficulty.value < 5:
            self.difficulty =  Difficulty_enum(self.difficulty.value + 1)
        else:
            self.difficulty = Difficulty_enum(1)

        self.load()