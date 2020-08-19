from .. import Achievements

class Achievement(object):
    def __init__(self, stat:str, condition:int, name:str, unlocked:int, path:str):
        """Achievement class"""
        self.stat = stat
        self.condition = condition
        self.name = name
        self.unlocked = unlocked
        self.path = path

    def unlock(self) -> None:
        '''
        Stat: the stat to check against
        Addition is an optional kwarg if achievement is checking for
        '''
        self.unlocked = 1

    def get_stat(self):
        '''
        stat: string to pass into query cached stats
        condition: value to meet
        '''
        return self.stat

    def get_path(self):
        """Get the path of the achievement sprite"""
        return self.path

    def reset(self) -> None:
        """Reset the unlocked state"""
        self.unlocked = 0

    def get_achieved(self):
        """Check if the achievement is unlocked"""
        return self.unlocked

    def unpack(self)-> tuple:
        '''
        Unpack for writing to database
        '''
        return self.stat,self.condition, self.name, self.unlocked

    def get_name(self):
        """Get the name of the achievement"""
        return self.name

    def check_achieved(self, stat:int, addition:int):
        '''
        Stat: amount currently in the database
        Addition: amount to check against
        '''

        #If the achievement is not yet unlocked and it meets condition
        if not self.unlocked and  (stat + addition >= self.condition):

            #Mark the achievement as unlocked
            self.unlock()

            #Return the achievement
            return self.__str__()
        
        return None

    def __str__(self):
        """String representation of the achievement"""
        return f"{self.name} : {'Unlocked' if self.unlocked else 'Locked'}"


class AchievementManager(object):
    def __init__(self, dbpath:str):
        """Main achievement manager class"""

        #Create Achievements class
        self.adb = Achievements(dbpath)

        #Get a list of achievements
        self.achievements = dict(map(lambda x: (x[1], Achievement(x[2], x[3], x[4], x[5], x[6])), self.adb.fetch_all()))

        #Get the stats
        self.stats = dict(map(lambda x: (x[1].get_stat(), x[0]), self.achievements.items()))

    def get_all(self):
        """Get the status of the achievements"""
        return dict(map(lambda x: (x.get_name(),x.get_achieved()), self.achievements.values()))

    def checkUnlocked(self, key:str, stat:int, stat2:int = 0):
        """Check if the stat is unlocked based on stat"""

        #Check if the achievement is valid
        ac = self.getAchievement(key)

        #If it is valid
        if ac:

            #Check if it is achieved
            return ac.check_achieved(stat, stat2)

    def getAchievement(self, key:str) -> Achievement:
        """Get the achievement"""
        return self.achievements.get(self.stats.get(key,None), None)

    def checkAchieved(self, stat:dict, state:dict) -> list:
        ''' Handles update of Achievement in real time as well as Achievement Popup '''
        unlocked = []

        #Iterate through all the acheivements
        for k in self.achievements.values():

            # Checks through list of achievements
            metric = k.get_stat()
            ac = self.checkUnlocked(k, stat.get(metric, 0), state.get(metric, 0))

            if ac:
                unlocked.append(ac)

        return unlocked


    def parseAchievement(self):
        '''
        Returns a list of tuples of Achievements achieved
        output: [ Long Text Name, 1/0 achieved, path ]
        '''
        return list(map(lambda x: (x.get_name(),x.get_achieved(), x.get_path()), self.achievements.values()))

    def reset(self):
        '''
        Reset Achievement State
        '''
        for i in self.achievements.values():
            i.reset()

    def __del__(self):
        """Destructor for the Achievement Manager"""
        for i,j in self.achievements.items():
            self.adb.update(i,j.get_achieved())

        self.adb.__del__()
