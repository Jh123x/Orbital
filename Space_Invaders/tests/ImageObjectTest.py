# Unit tests
import os
import sys
import unittest

import pygame

# Change directory to that of the main path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes import *


class ImageObjectTest(unittest.TestCase):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def testCase1(self):
        """
        Test case 1: Test the get_height
        """
        obj = ImageObject(0, 0, 10, 20, None, False)
        assert obj.get_height() == 20

    def testCase2(self):
        """
        Test case 2: Test the get_width
        """
        obj = ImageObject(0, 0, 10, 20, None, False)
        assert obj.get_width() == 10


if __name__ == "__main__":
    unittest.main()
