#Unit tests
import unittest
import os
import sys
#Change directory to that of the main path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes import *

#Relavant functions to be tested
class SettingsTester(unittest.TestCase):
    
    def setUp(self) ->None:
        """Set up for main class"""

        #Call the superclass setup
        super().setUp()

        #Read the config file from the settings
        self.config = read_settings(form_abs_path(__file__,"../settings.cfg"),"Space Invaders")

    def tearDown(self):
        """Tear down for the main class"""
        del self.config
        #Nothing to Teardown
        return super().tearDown()
    
    def testConfigA(self):
        """
        Test if config file is converted to a dictionary
        """
        assert type(self.config) == dict, "Read setting not returning a dictionary"

    def testConfigB(self):
        """
        Test For integer parsing and converting to correct type
        """
        assert type(self.config['sensitivity']) == int, "Not parsing and converting digit correctly"
    
    def testConfigC(self):
        """
        Test for boolean parsing and converting to correct type
        """
        assert type(self.config['debug']) == bool, "Not parsing string to boolean correctly"
    def testConfigD(self):
        """
        Test for string parsing properly
        """
        assert type(self.config['icon_img_path']) == str, "Not parsing string to correct type"

    def testConfigE(self):
        """
        Test if the game_width is correct
        """
        assert type(self.config['game_width']) == int, "Not parsing the game width correctly"

    def testConfigF(self):
        """
        Test if the game_height is loaded correctly
        """
        assert type(self.config['game_height']) == int, "Not parsing the game width correctly"

    def testConfigG(self):
        """
        Test if the maxfps is loaded correctly
        """
        assert type(self.config['maxfps']) == int


class AbsPathTest(unittest.TestCase):

    def testConfig1(self) -> None:
        """
        Test case 1: "C:\\hello1\\hello2" and "hello3\\hello4"
        """
        path1 = "C:\\hello1\\hello2"
        path2 = "hello3\\hello4"
        test1 = os.path.join(os.path.dirname(path1),path2)
        test2 = form_abs_path(path1,path2)
        assert test1 == test2, f"{test1} and {test2} is different"


class numFilesTest(unittest.TestCase):
    def testConfig1(self) -> None:
        """
        Test case 1: Number of files in current folder
        """
        assert len(os.listdir(os.path.dirname(__file__))) == len(list_dir(os.path.dirname(__file__))), "Results are not the same for the 2 functions"

class ConvertTypeTest(unittest.TestCase):
    def testConfig1(self) -> None:
        """
        Test case 1: Converting ("hello","3")
        """
        result = convertType(("hello","3"))
        assert type(result[0]) == str and type(result[1]) == int, '''("hello","3") is not converterd correctly'''

    def testConfig2(self) -> None:
        """
        Test case 2: Converting ("Hello", "world")
        """
        result = convertType(("Hello", "world"))
        assert type(result[0]) == str and type(result[1]) == str, '''("Hello", "world") is not converterd correctly'''


    def testConfig3(self) -> None:
        """
        Test case 3: Converting (3, "$")
        """
        result = convertType((3, "$"))
        assert type(result[0]) == int and type(result[1]) == str, '''(3, "$") is not converterd correctly'''

    def testConfig4(self) -> None:
        """
        Test case 4: Converting (3, "False")
        """
        result = convertType((3, "False"))
        assert type(result[0]) == int and type(result[1]) == bool, '''(3, "False") is not converterd correctly'''

    def testConfig5(self) -> None:
        """
        Test case 5: Converting ("False", "tRuE")
        """
        result = convertType(("False", "tRuE"))
        assert type(result[0]) == str and type(result[1]) == bool, '''("False", "tRuE") is not converterd correctly'''

    def testConfig6(self) -> None:
        """
        Test case 6: Converting (True, "12346")
        """
        result = convertType((True, "12346"))
        assert type(result[0]) == bool and type(result[1]) == int, '''(True, "12346") is not converterd correctly'''

    def testConfig7(self) -> None:
        """
        Test case 7: Converting ()
        """
        result = convertType(())
        assert result == (), '''() is not converterd correctly'''

    def testConfig8(self) -> None:
        """
        Test case 8: Converting (1,2,3,4)
        """
        result = convertType((1,2,3,4))
        assert result == (1,2,3,4), '''(1,2,3,4) is not converterd correctly'''

    def 

#Main function
if __name__ == "__main__":
    #Runs all of the tests defined above
    unittest.main()