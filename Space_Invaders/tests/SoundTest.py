#Unit tests
import unittest
import os
import sys

#Change directory to that of the main path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes import *

class testMusic(object):
    def __init__(self, name):
        self.name = name
        self.volume = 0
        self.played = False

    def play(self):
        self.played = True
        return self.name

    def set_volume(self, volume):
        self.volume = volume

    def __eq__(self, other):
        if type(self) != type(other):
            return super().__eq__(other)
        else:
            return self.name == other.name

class SoundTest(unittest.TestCase):

    def setUp(self):
        d = {'sound':testMusic("music")}
        self.sound = Sound(d, False, 0.5, False)
        return super().setUp()

    def tearDown(self):
        del self.sound
        return super().tearDown()

    def testCase1(self):
        """
        Test case 1: Test if the state of the sound is correct
        """
        assert self.sound.get_state() == False

    def testCase2(self):
        """
        Test case 2: Test if get_volume is correct
        """
        assert self.sound.get_volume() == 0.5

    def testCase3(self):
        """
        Test case 3: Test if the volume toggle is working
        """

        result = [0.5, 0.75, 1.00, 0.25, 0.5]
        for i in range(len(result)):
            assert self.sound.get_volume() == result[i]
            self.sound.volume_toggle()


    def testCase4(self):
        """
        Test case 4: Test if get_dict() method
        """
        assert self.sound.get_dict() == {'sound':testMusic("music")}

    def testCase5(self): 
        """
        Test case 5: Check if enable method is working
        """

        #Enable the sound
        self.sound.toggle()
        assert self.sound.get_state(), "Toggle on is not working"

        #Disable the sound
        self.sound.toggle()
        assert not self.sound.get_state(), "Toggle off is not working"

    def testCase6(self):
        """
        Test case 5: Test if the play method is correct
        """
        #Before toggling
        assert not self.sound.play('sound'), "Sound is not playing correctly"
        assert not self.sound.play('does not exist'), "Playing music that is not found"

        #Enable sound
        self.sound.toggle()

        #After toggling
        assert self.sound.play('sound'), "Sound is not playing correctly"
        assert not self.sound.play('does not exist'), "Playing music that is not found"



if __name__ == "__main__":
    unittest.main()
