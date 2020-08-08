#To manage the database
import os
import sqlite3

class Database(object):
    def __init__(self, dbpath:str, name:str):
        """Base database object"""
        #Store the name
        self.name = name

        #Store the database path
        self.dbpath = dbpath

        #Connect to the database
        self.connection = sqlite3.connect(dbpath, timeout=10)

        #Get the cursor of the database
        self.cursor = self.connection.cursor()

        #Cache
        self.cache = []
        self.changed = True

    def execute(self, command:str, *args) -> None:
        """Execute the SQL command in the form of a string"""

        #Run the command
        self.cursor.execute(command, *args)

    def is_cache(self) -> bool:
        """Check if there is a cached copy of the database"""
        return True if self.cache else False

    def fetch_all(self) -> tuple:
        """Fetch all the data from the table"""
        
        #If there is no cache or if there are changes in the cache
        if self.changed or not self.is_cache():
            
            #Fetch all the items in the table and add it to the cache
            self.cursor.execute(f"SELECT * FROM {self.name}", )
            self.cache = self.cursor.fetchall()

            #Make the changes as none
            self.changed = False

        #Return the items
        return self.cache

    def __del__(self):
        """Destructor for the Scoreboard
            Commits all the changes that is done
        """
        #Save all changes
        self.connection.commit()

class SettingsDB(Database):
    def __init__(self, dbpath:str):
        """Constructor for the settings db class"""
        #Call the superclass
        super().__init__(dbpath, 'settings')

        #Create the table if it does not exist
        self.execute("CREATE TABLE IF NOT EXISTS settings (id INTEGER, name TEXT, settings TEXT)")

        #Get the count of tables with the name
        self.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='settings' ''')
        bo = self.cursor.fetchone()[0]
        if bo == 0:
            """Add the relavant settings"""
            self.add("background",0)
            self.add("music",False)

    def add(self, name:str, setting:str) -> None:
        """Add the settings to the table"""
        #Insert the element into the table
        self.execute('INSERT INTO settings VALUES(?, ?, ?)', (None, name, setting))

        #Mark the database as changed
        self.changed = True

    def update(self, name:str, setting:str) -> None:
        """Update the value of the settings"""
        #Call the update function

        # print(settings)
        self.execute("UPDATE settings SET settings = ? WHERE name = ?", (setting,name))

        #Mark db as changed
        self.changed = True

    def remove(self, name:str) -> None:
        """Remove the last entry from the highscore board"""
        #Remove from the database where the name matches the name to be removed
        self.execute(f"DELETE FROM {self.name} WHERE name = ?", (name,))

        #Mark the database as changed
        self.changed = True


class Statistics(Database):
    def __init__(self, dbpath:str):
        """Class for keeping track of game statistics"""
        #Call the superclass
        super().__init__(dbpath, 'statistics')

        #Create the table if it does not exist
        self.execute("CREATE TABLE IF NOT EXISTS statistics (id INTEGER, name TEXT, value INTEGER)")

        self.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='statistics' ''')
        bo = self.cursor.fetchone()[0]

        if bo == 0:
            """Add the relevant settings"""
            self.add("sf", 0)
            self.add("en_k", 0)
            self.add("el_k", 0)
            self.add("sl", 0)
            self.add("pu", 0)
            self.add("mpu", 0)
            self.add("ek_c", 0)
            self.add("ek_e", 0)

    def add(self, name:str, stat:int) -> None:
        '''
        Add the related statistic into the table
        '''
        # Insert element into table
        self.execute('INSERT INTO statistics VALUES(?, ?, ?)', (None, name, stat))

        # Mark DB as changed
        self.changed = True

    def update(self,name:str, stat:int ) -> None:
        """Update the value of the settings"""
        # Call the update function
        # print(self.name)
        # print('name',name)
        # print('setting',stat)
        self.execute("UPDATE statistics SET value = ? WHERE name = ?", (stat, name))
        # (setting, name)
        # self.execute("UPDATE settings SET settings = ? WHERE name = ?", (setting,name))
        # Mark db as changed
        self.changed = True

    def remove(self, name: str) -> None:
        """Remove the last entry from the highscore board"""
        # Remove from the database where the name matches the name to be removed
        self.execute(f"DELETE FROM {self.name} WHERE name = ?", (name,))

        # Mark the database as changed
        self.changed = True

class Achievements(Database):
    def __init__(self, dbpath:str):
        """Class for keeping track of achievements"""
        #Call the superclass
        super().__init__(dbpath, 'achievement')

        #Create the table if it does not exist
        self.execute("CREATE TABLE IF NOT EXISTS achievement (id INTEGER, name TEXT, reward INTEGER, description TEXT, completed INTEGER)")

    def add(self, name:str, reward:int, description:str):
        """Add the achievement to the list"""
        #Insert the element into the table
        self.execute('INSERT INTO achievement VALUES(NULL, ?, ?, ?)', (name, reward, description))

        #Mark the database as changed
        self.changed = True

    def remove(self, name:str) -> None:
        """Remove the last entry from the highscore board"""
        #Remove from the database where the name matches the name to be removed
        self.execute(f"DELETE FROM {self.name} WHERE name = ?", (name,))

        #Mark the database as changed
        self.changed = True

class ScoreBoard(Database):
    def __init__(self, dbpath:str, max_length:int = 5):
        """Class for keeping track of the high score"""

        #Call the superclass
        super().__init__(dbpath, 'highscore')

        #Set the max number of highscore to be stored for the players
        self.max_length = max_length

        #Create the table if it does not exist
        self.execute("CREATE TABLE IF NOT EXISTS highscore (id INTEGER, name TEXT, score INTEGER)")

    def remove(self, name:str) -> None:
        """Remove the last entry from the highscore board"""
        #Remove from the database where the name matches the name to be removed
        self.execute(f"DELETE FROM {self.name} WHERE name = ?", (name,))

        #Mark the database as changed
        self.changed = True

    def remove_exact(self, name:str, score:int) -> None:
        """Removes the entry that matches both the name and the highscore"""

        #Remove the entry from the database
        self.execute("DELETE FROM highscore WHERE name = ? AND score = ?", (name, score))

        #Mark the database as changed
        self.changed = True

    def add(self, name:str, score:int) -> None:
        """Add a name and a score to the scoreboard"""
        #Insert the element into the table
        self.execute('INSERT INTO highscore VALUES(NULL, ?, ?)', (name,score))

        #Mark the database as changed
        self.changed = True

    def add_all(self, *args) -> None:
        """Add all the items into the database"""
        #If there is no cache update the cache
        if not self.is_cache():
            self.fetch_all()

        #Iterate through each of the items 
        for item in args:

            #Add them if they are not in the cache
            if item not in self.cache:

                #Add to the database and the cache
                self.add(item[1],item[2])
                self.cache.append(item)

    def remove_all(self, *args):
        """Remove all the items from the table"""
        #Call the cache
        if not self.is_cache():
            self.fetch_all()

        #For each of the items
        for item in args:

            #If the item is in the cache remove it
            if item in self.cache:
                self.remove_exact(item[1], item[2])


def main() -> None:
    """The main function for the database class used for debuging and modifying database"""

    #Load the path of the database
    dbpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..', '..','..' ,'data', 'test.db')
    # print(dbpath)
    #Create the scoreboard database
    db = ScoreBoard(dbpath)
    ac = Achievements(dbpath)
    s = SettingsDB(dbpath)
    stat = Statistics(dbpath)

    #For debugging
    print(f"Running the main function from database file")
    print(f"Scoreboard db created")

    #Create a while loop for the user to test commands as they are typed into the terminal
    while(True):

        #Print entries
        print(f"Highscore: {db.fetch_all()}")
        print(f"Achievements: {ac.fetch_all()}")
        print(f"Settings: {s.fetch_all()}")
        print(f"Stats: {stat.fetch_all()}" )

        
        #Get commands from user
        try:
            command = input("Type in the command: ").strip()
            if command == 'q':
                break
            print(eval(command))
        
        #If there is an error print the error message
        except Exception as exp:
            print(exp)


#If the function is run as the main file call the main function
if __name__ == "__main__":
    main()