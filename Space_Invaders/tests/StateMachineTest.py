# Unit tests
import os
import sys
import unittest

import pygame

# Change directory to that of the main path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes import *


class StateMachineTester(unittest.TestCase):

    def setup(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def testCase1(self):
        '''
        Test case 1: assert that initial state of StateMachine is 0
        '''
        sm = StateMachine(1)
        assert sm.get_state() == 0

    def testCase2(self):
        '''
        Test Case 2: Assert that only player entity info is essential for AI functionality
        '''
        sm = StateMachine(1)
        e = {'mobs': [], 'bosses': [], 'bullets': [], 'enemy_player': 'None',
             'player': (400, 200, 1)}
        # simulates initialisation condition of screen

        sm.state_check(e)
        assert sm.get_state() == 1

    def testCase3(self):
        '''
        Test case 3: assert that state changes after a set n ticks with a given entity list
        '''
        sm = StateMachine(2)
        e = {'mobs': [(400, 300)], 'bosses': [(400, 300)], 'bullets': [(350, 200)], 'enemy_player': 'None',
             'player': (400, 200, 1)}

        # Check that no state was changed from 1 time step
        sm.state_check(e)
        assert sm.get_state() == 0
        sm.state_check(e)
        # Check that state was changed after 2 ticks
        assert sm.get_state() == 2
        sm.state_check(e)
        sm.state_check(e)
        # Check that an secondary state transition occured due to given entity inputs
        assert sm.get_state() == 1

    def testCase4(self):
        '''
        Test case 4: assert that state changes when presented with differing conditions of input
        '''
        sm = StateMachine(1)
        e1 = {'mobs': [(350, 200)], 'bosses': [], 'bullets': [], 'enemy_player': 'None',
              'player': (350, 200, 2)}
        sm.state_check(e1)
        assert sm.get_state() == 1
        e2 = {'mobs': [], 'bosses': [], 'bullets': [], 'enemy_player': 'None',
              'player': (350, 200, 3)}
        sm.state_check(e2)
        assert sm.get_state() == 0
        e3 = {'mobs': [(300, 400)], 'bosses': [], 'bullets': [], 'enemy_player': 'None',
              'player': (350, 200, 1)}

        assert sm.get_state() == 2
