#Unit tests
import unittest
import os
import sys

#Change directory to that of the main path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes import *


class ScreenTest(unittest.TestCase):

    def setUp(self):
        self.screen = Screen(600, 800, State.NONE, None, 0, 0, False)
        return super().setUp()

    def tearDown(self):
        del self.screen
        return super().tearDown()

    def testCase1(self):
        """
        Test case 1: Check if set state is working
        """

        #Check if the current state is correct
        assert self.screen.state == State.NONE

        #Change the state
        self.screen.set_state(State.QUIT)

        #Check if the State is changed
        assert self.screen.state == State.QUIT

if __name__ == "__main__":
    unittest.main()