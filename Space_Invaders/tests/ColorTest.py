#Unit tests
import unittest
import os
import sys

#Change directory to that of the main path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes import *


class ColorTest(unittest.TestCase):
    """Testing the if the colors are accurate"""

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def testCase1(self):
        """
        Test case 1: White color
        """
        assert WHITE == (255,255,255), "White color is off"

    def testCase2(self):
        """
        Test case 2: Grey color
        """
        assert GREY == (60, 60, 60), "Grey color is off"

    def testCase3(self):
        """
        Test case 3: Black color
        """
        assert BLACK == (0, 0, 0), "Black color is off"

    def testCase4(self):
        """
        Test case 4: Red color
        """
        assert RED == (255, 0, 0), "Red color is off"

    def testCase5(self):
        """
        Test case 5: Blue color
        """
        assert BLUE == (0, 0, 255), "Blue color is off"

    def testCase6(self):
        """
        Test case 6: Green color
        """
        assert GREEN == (0, 128, 0), "Green color is off"

    def testCase7(self):
        """
        Test case 7: Lime color
        """
        assert LIME == (0, 255, 0), "Lime color is off"

    def testCase8(self):
        """
        Test case 8: Yellow color
        """
        assert YELLOW == (255, 255, 0), "Yellow color is off"


if __name__ == "__main__":
    unittest.main()

