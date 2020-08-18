from . import AchievementManager
from .. import Popup, Screen, Statistics

class AchievmentTracker(object):

    def __init__(self, db_path:str, popup_q):
        """Acheivement tracker class"""
        self.statdb = Statistics(db_path)
        self.stats = dict(map(lambda x: x[1:], self.statdb.fetch_all()))
        self.long_form = {
            'ek_c': "Number of Enemies Killed in Classic",
            'ek_e': "Number of Enemies Killed in Endless",
            'el_k': "Number of Elite Enemies killed",
            'en_k': "Number of Enemies killed",
            'sl'  : "Number of Ships wrecked",
            'pu'  : "Number of Powerups used", 
            'sf'  : "Number of Shots Fired", 
            'mpu' : "Max Powerups used",
                        }
        self.manager = AchievementManager(db_path)
        self.popup_q = popup_q

    def get_all(self):
        """Gets all the key value pairs"""
        return [self.get_statistic(item) for item in self.long_form]

    def get_statistic(self, key) -> tuple:
        '''Get Key Value Pair of Longform statistic'''
        return self.get_longform(key),self.get_stat(key)

    def set_value(self, key:str, value:int) -> None:
        """Set the value"""
        self.stats[key] = value

    def add_popup(self, name:str):
        """Add the popup with the name"""
        #Add the popup with the name for 2 seconds
        self.popup_q.add(name, 2)

    def update_achievement(self, state:dict = {}) -> list:
        '''Message Passing down to achievment manager'''
        print('my_stats',self.stats)
        print('incoming',state)
        lst = self.manager.checkAchieved(self.stats,state)
        for achievement in lst:
            self.popup_q.add(achievement, 2)

    def get_stat(self, key:str):
        '''Getter to retrieve tracked statistic'''
        return self.stats.get(key, None)

    def get_longform(self, key):
        '''Getter to retrieve longform text of tracked statistic for display'''
        return self.long_form.get(key,None)

    def add_value(self, key:str, value:int) -> None:
        ''' Add Value to Specific Statistic'''
        self.stats[key] += value

    def set_max_value(self, key:str, value:int) -> None:
        ''' Set Value of Stat to max of current value vs given value'''
        self.stats[key] = max(self.stats[key], value)

    def shot_fired(self, value:int) -> None:
        ''' Add value to accumulated number of shots fired by player'''
        self.add_value('sf',value)

    def enemies_killed(self, value:int) -> None:
        ''' Add value to accumulated number of enemies killed '''
        self.add_value('en_k',value)

    def elites_killed(self, value:int) -> None:
        '''Add value to accumulated number of elite monsters killed'''
        self.add_value('el_k', value)

    def ships_destroyed(self, value:int) -> None:
        '''Add value to accumulated number of ships destroyed'''
        self.add_value('sl', value)

    def powerups_used(self, value:int) -> None:
        '''Add value to accumulated statistic of Powerups used'''
        self.add_value('pu', value)

    def max_powerups_used(self, value:int) -> None:
        '''Compare current value of powerups used vs incoming value'''
        self.set_max_value('mpu', value)

    def enemies_killed_in_classic(self, value:int) -> None:
        '''Compare current value of enemies killed in Classic vs incoming value'''
        self.set_max_value('ek_c', value)

    def enemies_killed_in_endless(self, value:int) -> None:
        '''Compare current value of enemies killed in Endless vs incoming value'''
        self.set_max_value('ek_e', value)

    def reset(self) -> None:
        '''function to reset statistics accumulated'''
        for k in self.stats:
            self.stats[k] = 0

    def reset_achieved(self):
        """Reset the achievement"""
        self.manager.reset()

    def check_unlocked(self, key:str, stat1:int) -> str:
        """Check if the achievement is unlocked based on key and stat"""

        #Get the achievement if it is achieved
        achievement = self.manager.checkUnlocked(key, stat1)

        #If there is an achievement
        if achievement:

            #Add the achievement to the popup queue to be shown
            self.popup_q.add(achievement, 2)

    def __del__(self) -> None:
        """Destructor for the Achievement tracker"""
        # Writes cached values into the database
        for k,v in self.stats.items():
            self.statdb.update(k,v)

        self.statdb.__del__()

        self.manager.__del__()


