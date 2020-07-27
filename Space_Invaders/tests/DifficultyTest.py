#Unit tests
import unittest
import os
import sys

#Change directory to that of the main path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes import *

class DifficultyTest(unittest.TestCase):

    def setUp(self):
        
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def testCase1(self):
        """
        Test case 1: Check if get multiplier returns an int
        """
        self.difficulty = Difficulty(1)
        assert type(self.difficulty.get_multiplier(1)) == int

    def testCase2(self):
        """
        Test case 2: Check if the value is correct
        """

        #Check the value for range between [1, 6]
        for i in range(1, 7):
            assert Difficulty(i).value == i

    def testCase3(self):
        """
        Test case 3: Check if the names are correct
        """

        names = ["CASUAL", "EASY", "MEDIUM", "HARD", "IMPOSSIBLE", "OUTRAGEOUS"]
        for i in range(1, 7):
            d = Difficulty(i)
            assert d.name == names[i-1], f"Name {d.name} is not {names[i]}"



if __name__ == "__main__":
    unittest.main()