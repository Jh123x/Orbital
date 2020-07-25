import sqlite3
import os
import unittest
from ..classes import Database,ScoreBoard,Achievements,SettingsDB

class DatabaseTest(unittest.TestCase):

    def setup(self):
        dbpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'data', 't.db')
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def testCase1(self):
        pass



if __name__ == '__main__':
    unittest.main()
