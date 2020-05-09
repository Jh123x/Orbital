#Unit tests
import unittest
import os, sys
#Import the main file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import read_settings

#Relavant functions to be tested
class MainFileTester(unittest.TestCase):
    
    def setUp(self) ->None:
        """Set up for main class"""
        super().setUp()
        self.config = read_settings("settings.cfg","Space Invaders")


    def tearDown(self):
        """Tear down for the main class"""
        #Nothing to Teardown
        return super().tearDown()
    
    def testConfigA(self):
        """
        Test if config file is converted to a dictionary
        """
        assert type(self.config) == dict, "read setting not returning a dictionary"

    def testConfigB(self):
        """
        Test For integer parsing and converting to correct type
        """
        assert type(self.config['sensitivity']) == int, "not parsing and converting digit correctly"
    
    def testConfigC(self):
        """
        Test for boolean parsing and converting to correct type
        """
        assert type(self.config['debug']) == bool, "not parsing string to boolean correctly"
    def testConfigD(self):
        """
        Test for string parsing properly
        """
        assert type(self.config['icon_img_path']) == str, "not parsing string to correct type"


#game window, 
#Test Classes
'''
class GameClassTest(unittest.TestCase):
    """Unit Test for the Game Class"""
    def setUp(self) -> None:
        """To be called before the testing for all the testcases"""
        

    def tearDown(self) -> None:
        """To be called after testing all the testcases"""
        pass

    def test1(self) -> None:
        """First Test case
            assert a test within the function
            EG: assert foo+foo = 64
        """
        assert 1 == 0, "Test 1 has failed"

class BulletClassTest(unittest.TestCase):
    """Unit test for the bullets"""

    def setUp(self) -> None:
        """To be called before every test case"""
        pass

    def tearDown(self) -> None:
        """To be called after every test case"""
        pass
    
    def testA(self) -> None:
        """
        Enemy Bullet Hits ground
        """
        assert 1 == 1, "This test has passed"
    def testB(self) -> None:
        """
        Player Bullet hits end of Screen
        """
    def testC(self) -> None:
        """
        Player Hits Enemy Alien
        """
    def testD(self) -> None:
        """
        Player Hit by enemy bullet
        """

'''
#Main function
if __name__ == "__main__":
    #Runs all of the tests defined above
    unittest.main()