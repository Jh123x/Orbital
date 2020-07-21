import math
import numpy as np


def calc_dist(p1, p2):
    '''
    Calculate distance between point 1 and point 2
    '''
    return np.sqrt((p2[0] - p1[0]) ** 2 +
                     (p2[1] - p1[1]) ** 2)

def phi(x):
    'Cumulative distribution function for the standard normal distribution'
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

class StateMachine:
    def __init__(self, tick):
        '''
        ticks: The number of ticks between state transitions
        state: Integer value of state which determines behaviour
        Possible States:
            0: Idle/Initialised
            1: Aggressive Mode
            2: Defensive Mode
        clock: internal clock of movement
        position: stores current player position
        '''
        self.state = 0
        self.tick = tick
        self.clock = 0
        self.life = 3
        self.position = None
        self.movement = 0
        self.nearest_bullet = 0

    def state_check(self, entities):
        # Increment Clock tick
        self.clock = (self.clock+1) % self.tick
        self.life = entities['player'][2]
        self.position = entities['player'][:2]
        self.nearest_bullet = min(entities['bullets'],key=lambda x: calc_dist(self.position, x), default=(-1, -1))
        if self.clock == 0:
            # If Clock reaches limit, check environment and change state of AI Model
            return self.state_change(entities)

        else:
            # Take an action according to the state and entities
            return self.action(entities)

    def state_change(self,entities):
        nearest_boss_loc = min(list(map(lambda x: calc_dist(self.position, x), entities['bosses'])), default=1000)
        nearest_mob_loc = min(list(map( lambda x: calc_dist(self.position, x) ,entities['mobs'])), default=1000)

        if self.state == 0:

            # If mobs are far away and have a lot of life, go to aggressive behaviour
            if self.life > 1 and (nearest_mob_loc > 400 or nearest_boss_loc > 500 ):
                self.state = 1
            # If mobs are far but life is low, enter defensive behaviour
            elif self.life == 1 and (nearest_mob_loc < 400 or nearest_boss_loc < 500 ):
                self.state = 2

        elif self.state == 1:
            #if mobs are moderately far away and lives not 1
            if self.life > 1 or (nearest_mob_loc > 300 or nearest_boss_loc > 400 ):
                self.state = 0
            # if life is 1 but enemy position is dire, maintain aggression
            elif self.life == 1 and not (nearest_boss_loc <200 or nearest_boss_loc <300):
                self.state = 1
        else:
            if self.life >1 and (nearest_mob_loc > 300 or nearest_boss_loc > 400 ):
                self.life = 0
            elif self.life == 1 and (nearest_boss_loc <200 or nearest_boss_loc <300):
                self.state = 1
        return self.action(entities)


    def action(self,entities):
        # with the current state, take actions according to the current policy
        if self.state == 0:
            return self.balanced(entities)

        elif self.state == 1:
            return self.aggressive(entities)

        else:
            return self.defensive(entities)

    def dodging_decision_control(self):
        # normalising position of player
        middle = (self.position[0] - 300) / 300
        # Using middle of screen as the base position of player, dodge with respect to
        # current position relative to the base position

        prob = 0.05

        # if random value > prob, take action from left set
        if self.clock != 0:
            direction = self.nearest_bullet[0] - self.position[0]
            rand = np.random.rand()
            if self.nearest_bullet == (-1, -1) or rand < prob:
                self.movement = np.random.choice([1, 2, 3, 4, 5], p=[0.325, 0.325, 0.05, 0.15, 0.15])
            elif direction >= 0 and rand > prob:
                self.movement = np.random.choice([ 1, 3, 4],p=[ 0.65, 0.05, 0.3])
            elif direction < 0 and rand > prob:
                # Take action from right movement set
                self.movement = np.random.choice([2, 3, 5], p = [0.65, 0.05, 0.3])
        # If current position is beyond set boundaries, move back to centralise bounds
        if self.position[0] >550:
            self.movement = np.random.choice([ 1, 3, 4],p=[ 0.65, 0.05, 0.3])
        elif self.position[0]<50:
            self.movement = np.random.choice([1, 3, 4], p=[0.65, 0.05, 0.3])
        return self.movement

    def balanced(self,entities):
        # {'mobs': enemy1, 'bosses': enemy2, 'bullets': eb, 'enemy_player': ep, 'player': (curr_x, curr_y)}
        # (self.shoot, self.move_left, self.move_right, lambda: 1, self.move_shoot(True),
        #                 self.move_shoot(False))

        # If there is a enemy above but no bullets above, shoot
        #print(entities)
        if len(entities['bullets'])==0 and (len(entities['mobs']) != 0 or len(entities['bosses']) != 0
                                            or entities['enemy_player'] != 'None'):
            return np.random.choice([0 , 3, 4, 5],p = [0.4 ,0.1 ,0.25,0.25])
        # Determine if the ai will take a random action or take a smart decision
        rand = np.random.rand()
        nearest_bullet_loc = min(list(map(lambda x: calc_dist(self.position,x),entities['bullets'])),default=1000)
        # If bullet is nearby, move away
        if nearest_bullet_loc < 300 and rand > 0.5:
            return self.dodging_decision_control()
        nearest_boss_loc = min(list(map(lambda x: calc_dist(self.position,x), entities['bosses'])),default=1000)
        nearest_mob_loc = min(list(map(lambda x: calc_dist(self.position,x),entities['mobs'])),default=1000)
        # if a mob is closeby, perform a shooting action
        if (nearest_mob_loc < 400 or nearest_boss_loc < 500 or entities['enemy_player'] != 'None') and rand < 0.85:
            return np.random.choice([ 0, 3, 4, 5], p = [0.2, 0.1, 0.35, 0.35])
        else:
            return np.random.choice([ 0, 1, 2, 3, 4, 5], p=[0.2, 0.1, 0.15, 0.05, 0.25, 0.25])

    def aggressive(self, entities):
        # {'mobs': enemy1, 'bosses': enemy2, 'bullets': eb, 'enemy_player': ep, 'player': (curr_x, curr_y, life)}
        # (self.shoot, self.move_left, self.move_right, lambda: 1, self.move_shoot(True),
        #                 self.move_shoot(False))

        # If there is a enemy above but no bullets above, shoot
        if len(entities['bullets'])==0 and (len(entities['mobs']) != 0 or len(entities['bosses']) != 0
                                            or entities['enemy_player'] != 'None'):
            return np.random.choice([0 , 3, 4, 5],p = [0.4 ,0.1 ,0.25,0.25])
        # Determine if the ai will take a random action or take a smart decision
        rand = np.random.rand()
        nearest_bullet_loc = min(list(map(lambda x: calc_dist(self.position,x) ,entities['bullets'])),default=1000)
        # If bullet is nearby, move away
        if nearest_bullet_loc < 200 and rand < 0.85:
            return self.dodging_decision_control()
        nearest_boss_loc = min(list(map(lambda x: calc_dist(self.position,x), entities['bosses'])),default=1000)
        nearest_mob_loc = min(list(map(lambda x: calc_dist(self.position,x) ,entities['mobs'])),default=1000)
        # if a mob is closeby, perform a shooting action
        if (nearest_mob_loc < 400 or nearest_boss_loc < 500 or entities['enemy_player'] != 'None') and rand < 0.25:
            return np.random.choice([0, 3, 4, 5], p=[0.2, 0.1, 0.35, 0.35])
        else:
            return np.random.choice([0, 1, 2, 3, 4, 5], p=[0.2, 0.1, 0.15, 0.05, 0.25, 0.25])

    def defensive(self,entities):
        # {'mobs': enemy1, 'bosses': enemy2, 'bullets': eb, 'enemy_player': ep, 'player': (curr_x, curr_y, life)}
        # (self.shoot, self.move_left, self.move_right, lambda: 1, self.move_shoot(True),
        #                 self.move_shoot(False))

        # If there is a enemy above but no bullets above, shoot
        if len(entities['bullets'])==0 and (len(entities['mobs']) != 0 or len(entities['bosses']) != 0
                                            or entities['enemy_player'] != 'None'):
            return np.random.choice([0, 3, 4, 5], p=[0.4, 0.1, 0.25, 0.25])
        # Determine if the ai will take a random action or take a smart decision
        rand = np.random.rand()
        nearest_bullet_loc = min(list(map(lambda x: calc_dist(self.position,x) ,entities['bullets'])),default=1000)
        # If bullet is nearby, move away
        if nearest_bullet_loc < 400 and rand < 0.85:
            return self.dodging_decision_control()
        nearest_boss_loc = min(list(map(lambda x: calc_dist(self.position,x) ,entities['bosses'])),default=1000)
        nearest_mob_loc = min(list(map(lambda x: calc_dist(self.position,x) ,entities['mobs'])),default=1000)
        # if a mob is closeby, perform a shooting action
        if (nearest_mob_loc < 400 or nearest_boss_loc < 500 or entities['enemy_player'] != 'None') and rand < 0.35:
            return np.random.choice([0, 3, 4, 5], p=[0.2, 0.1, 0.35, 0.35])
        else:
            return np.random.choice([0, 1, 2, 3, 4, 5], p=[0.2, 0.1, 0.15, 0.05, 0.25, 0.25])







# if __name__ == '__main__':
#     machine = StateMachine(3)
#     e1 = {'mobs': [(400,300)], 'bosses': [(400,300)], 'bullets': [(350,200)], 'enemy_player': 'None', 'player': (400, 200 , 1)}
#
#     for i in range(18):
#         print(machine.state_check(e1))
#         print('state',machine.state)
