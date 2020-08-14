from . import Achievements

class Achievement(object):
    def __init__(self, stat:str, condition:int, name:str, unlocked:int, path:str):
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
        #TODO put the popup here for achieving the current achievement
        print('achieved', self.name)

    def get_stat(self):
        '''
        stat: string to pass into query cached stats
        condition: value to meet
        '''
        return self.stat

    def get_path(self):
        return self.path

    def reset(self) -> None:
        self.unlocked = 0

    def get_achieved(self):
        return self.unlocked

    def unpack(self)-> tuple:
        '''
        Unpack for writing to database
        '''
        return self.stat,self.condition, self.name, self.unlocked

    def get_name(self):
        return self.name

    def check_achieved(self, stat:int, addition:int = 0):
        '''
        Stat: amount currently in the database
        Addition: amount to check against
        '''
        print('hi from achievement')
        print(not self.unlocked)
        print('achieved status',stat + addition >= self.condition)
        if not self.unlocked and  (stat + addition >= self.condition):
            self.unlock()

    def __str__(self):
        return f"{self.name} : {'Unlocked' if self.unlocked else 'Locked'}"


class AchievementManager(object):
    def __init__(self, dbpath:str):
        self.adb = Achievements(dbpath)
        self.achievements = dict(map(lambda x: (x[1], Achievement(*x[2:])), self.adb.fetch_all()))
        self.stats = dict(map(lambda x: (x[0],x[1].get_stat()), self.achievements.items()))
        print(self.achievements)
    def checkAchieved(self, stat:dict, state:dict) -> None:
        ''' Handles update of Achievement in real time as well as Achievement Popup '''
        for k in self.achievements:
            # Checks through list of achievements
            metric = self.achievements[k].get_stat()
            self.achievements[k].check_achieved(stat.get(metric, 0), state.get(metric, 0))

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
        for i,j in self.achievements.items():
            self.adb.update(i,j.get_achieved())

        self.adb.__del__()
