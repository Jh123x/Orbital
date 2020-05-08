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
        #Nothing to setup
        return super().setUp()

    def tearDown(self):
        """Tear down for the main class"""
        #Nothing to Teardown
        return super().tearDown()

    def testConfig(self):
        pass


#Test Classes
class GameClassTest(unittest.TestCase):
    """Unit Test for the Game Class"""
    def setUp(self) -> None:
        """To be called before the testing for all the testcases"""
        pass

    def tearDown(self) -> None:
        """To be called after testing all the testcases"""
        pass

    def test1(self) -> None:
        """First Test case
            assert a test within the function
            EG: assert foo+foo = 64
        """
        assert 1 == 1

class BulletClassTest(unittest.TestCase):
    """Unit test for the bullets"""

    def setUp(self) -> None:
        """To be called before every test case"""
        pass

    def tearDown(self) -> None:
        """To be called after every test case"""
        pass

    def testA(self) -> None:
        """First Test case
            assert a test within the function
            EG: assert foo+foo = 64
        """
        assert 1 == 1





#Main function
if __name__ == "__main__":
    #Runs all of the tests defined above
    unittest.main()
