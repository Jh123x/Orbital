#Unit tests
import os
import unittest
import sys
import pygame


#Change directory to that of the main path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes import *

class BaseObjectTester(unittest.TestCase):

    def setup(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def testCase1(self):
        """
        Test case 1: Check get coord method
        """
        obj = BaseObject(0, 0, False)
        assert obj.get_coord() == (0,0)

    def testCase2(self):
        """
        Test case 2: Check the set coord method
        """
        obj = BaseObject(0, 0, False)
        obj.set_coord((1,2))
        assert obj.get_coord() == (1,2)

    def testCase3(self):
        """
        Test case 3: Check the get_x method
        """
        obj = BaseObject(0, 0, False)
        assert obj.get_x() == 0

    def testCase4(self):
        """
        Test case 4: Check the get_y method
        """
        obj = BaseObject(0, 1, False)
        assert obj.get_y() == 1

#Main function to run the tests
if __name__ == "__main__":
    unittest.main()



    