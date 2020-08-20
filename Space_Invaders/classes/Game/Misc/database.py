# To manage the database
import os
import sqlite3


class Database(object):
    def __init__(self, dbpath: str, name: str):
        """Base database object"""
        # Store the name
        self.name = name

        # Store the database path
        self.dbpath = dbpath

        # Connect to the database
        self.connection = sqlite3.connect(dbpath, timeout=10)

        # Get the cursor of the database
        self.cursor = self.connection.cursor()

        # Cache
        self.cache = []
        self.changed = True

    def execute(self, command: str, *args) -> None:
        """Execute the SQL command in the form of a string"""

        # Run the command
        self.cursor.execute(command, *args)

    def is_cache(self) -> bool:
        """Check if there is a cached copy of the database"""
        return True if self.cache else False

    def fetch_all(self) -> tuple:
        """Fetch all the data from the table"""

        # If there is no cache or if there are changes in the cache
        if self.changed or not self.is_cache():
            # Fetch all the items in the table and add it to the cache
            self.cursor.execute(f"SELECT * FROM {self.name}", )
            self.cache = self.cursor.fetchall()

            # Make the changes as none
            self.changed = False

        # Return the items
        return self.cache

    def __del__(self):
        """Destructor for the Scoreboard
            Commits all the changes that is done
        """
        # Save all changes
        self.connection.commit()


class SettingsDB(Database):
    def __init__(self, dbpath: str):
        """Constructor for the settings db class"""
        # Call the superclass
        super().__init__(dbpath, 'settings')

        # Create the table if it does not exist
        self.execute("CREATE TABLE IF NOT EXISTS settings (id INTEGER, name TEXT, settings TEXT)")

        # Get the count of tables with the name
        self.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='settings' ''')
        bo = self.cursor.fetchone()[0]
        if bo == 0:
            """Add the relavant settings"""
            self.add("background", 0)
            self.add("music", False)

    def add(self, name: str, setting: str) -> None:
        """Add the settings to the table"""
        # Insert the element into the table
        self.execute('INSERT INTO settings VALUES(?, ?, ?)', (None, name, setting))

        # Mark the database as changed
        self.changed = True

    def update(self, name: str, setting: str) -> None:
        """Update the value of the settings"""
        # Call the update function

        # print(settings)
        self.execute("UPDATE settings SET settings = ? WHERE name = ?", (setting, name))

        # Mark db as changed
        self.changed = True

    def remove(self, name: str) -> None:
        """Remove the last entry from the highscore board"""
        # Remove from the database where the name matches the name to be removed
        self.execute(f"DELETE FROM {self.name} WHERE name = ?", (name,))

        # Mark the database as changed
        self.changed = True


class Statistics(Database):
    def __init__(self, dbpath: str):
        """Class for keeping track of game statistics"""
        # Call the superclass
        super().__init__(dbpath, 'statistics')

        # Create the table if it does not exist
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
            self.add('tut_n_clr', 0)
            self.add('st_1_clr', 0)
            self.add('st_2_clr', 0)
            self.add('st_3_clr', 0)
            self.add('st_4_clr', 0)
            self.add('st_5_clr', 0)
            self.add('st_6_clr', 0)
            self.add('coop', 0)
            self.add('pvp', 0)
            self.add('aivs', 0)
            self.add('aicoop', 0)

    def add(self, name: str, stat: int) -> None:
        '''
        Add the related statistic into the table
        '''
        # Insert element into table
        self.execute('INSERT INTO statistics VALUES(?, ?, ?)', (None, name, stat))

        # Mark DB as changed
        self.changed = True

    def update(self, name: str, stat: int) -> None:
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
    def __init__(self, dbpath: str):
        """Class for keeping track of achievements"""
        # Call the superclass
        super().__init__(dbpath, 'achievement')

        # Create the table if it does not exist
        # Template format: ID, Short form Name of achievement, Statistic, Long Text of Achievement, 1/0 on whether completed
        self.execute(
            "CREATE TABLE IF NOT EXISTS achievement (id INTEGER, name TEXT, stat TEXT , condition INTEGER , description TEXT, completed INTEGER, img TEXT)")

        self.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='achievement' ''')
        bo = self.cursor.fetchone()

        if bo == 0:
            self.add("low", 'tut_n_clr', 1, 'A new low....', 'path')
            self.add("gr", 'st_1_clr', 1, 'Back from the Grave')
            self.add('man', 'st_2_clr', 1, 'One small step for Man...', 'path')
            self.add('mars', 'st_4_clr', 1, 'Mars Colony', 'path')
            self.add('back', 'st_5_clr', 1, 'Beat them Back')
            self.add('sky_net', 'st_6_clr', 1, 'Sk-...Cloud Net !!??', 'path')
            self.add('taste', 'en_k', 1, 'The First taste of Victory', 'path')
            self.add('hero', 'en_k', 1000, 'Hero of Humanity', 'path')
            self.add('monst', 'en_k', 5000, 'Are you a Monster??', 'path')
            self.add('sp_d', 'ek_e', 150, 'Space Defender', 'path')
            self.add('sp_inv', 'ek_c', 100, 'Master of Space Invaders', 'path')
            self.add('ck', 'coop', 10, 'Coop King', 'path')
            self.add('no_u', 'pvp', 10, "No, I'm the Space Defender!"), 'path'
            self.add('be_back', 'aicoop', 10, "I’ll Be Back", 'path')
            self.add('replace', 'aicoop', 10, 'Am I getting Replaced?', 'path')

    def add(self, name: str, stat: str, condition: int, description: str, path='path'):
        """Add the achievement to the list"""
        # Insert the element into the table
        self.execute('INSERT INTO achievement VALUES(NULL, ?, ?, ?, ?, ?, ?)',
                     (name, stat, condition, description, 0, path))

        # Mark the database as changed
        self.changed = True

    def remove(self, name: str) -> None:
        """Remove the last entry from the highscore board"""
        # Remove from the database where the name matches the name to be removed
        self.execute(f"DELETE FROM {self.name} WHERE name = ?", (name,))

        # Mark the database as changed
        self.changed = True

    def update(self, name: str, completed: int):
        self.execute("UPDATE achievement SET completed = ? WHERE name = ?", (completed, name))

        self.changed = True


class ScoreBoard(Database):
    def __init__(self, dbpath: str, max_length: int = 5):
        """Class for keeping track of the high score"""

        # Call the superclass
        super().__init__(dbpath, 'highscore')

        # Set the max number of highscore to be stored for the players
        self.max_length = max_length

        # Create the table if it does not exist
        self.execute("CREATE TABLE IF NOT EXISTS highscore (id INTEGER, name TEXT, score INTEGER)")

    def remove(self, name: str) -> None:
        """Remove the last entry from the highscore board"""
        # Remove from the database where the name matches the name to be removed
        self.execute(f"DELETE FROM {self.name} WHERE name = ?", (name,))

        # Mark the database as changed
        self.changed = True

    def remove_exact(self, name: str, score: int) -> None:
        """Removes the entry that matches both the name and the highscore"""

        # Remove the entry from the database
        self.execute("DELETE FROM highscore WHERE name = ? AND score = ?", (name, score))

        # Mark the database as changed
        self.changed = True

    def add(self, name: str, score: int) -> None:
        """Add a name and a score to the scoreboard"""
        # Insert the element into the table
        self.execute('INSERT INTO highscore VALUES(NULL, ?, ?)', (name, score))

        # Mark the database as changed
        self.changed = True

    def add_all(self, *args) -> None:
        """Add all the items into the database"""
        # If there is no cache update the cache
        if not self.is_cache():
            self.fetch_all()

        # Iterate through each of the items
        for item in args:

            # Add them if they are not in the cache
            if item not in self.cache:
                # Add to the database and the cache
                self.add(item[1], item[2])
                self.cache.append(item)

    def remove_all(self, *args):
        """Remove all the items from the table"""
        # Call the cache
        if not self.is_cache():
            self.fetch_all()

        # For each of the items
        for item in args:

            # If the item is in the cache remove it
            if item in self.cache:
                self.remove_exact(item[1], item[2])


def main() -> None:
    """The main function for the database class used for debuging and modifying database"""

    # Load the path of the database
    dbpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', 'data', 'test.db')
    # print(dbpath)
    # Create the scoreboard database
    db = ScoreBoard(dbpath)
    ac = Achievements(dbpath)
    s = SettingsDB(dbpath)
    stat = Statistics(dbpath)

    # For debugging
    print(f"Running the main function from database file")
    print(f"Scoreboard db created")

    # Create a while loop for the user to test commands as they are typed into the terminal
    while (True):

        # Print entries for all of the databases
        print(f"Highscore: {db.fetch_all()}")
        print(f"Achievements: {ac.fetch_all()}")
        print(f"Settings: {s.fetch_all()}")
        print(f"Stats: {stat.fetch_all()}")

        try:

            # Get commands from the user
            command = input("Type in the command: ").strip()

            # IF the player wants to quit
            if command == 'q':
                # Break out of the loop
                break

            # Otherwise evaluate the command
            print(eval(command))

        # If there is an error
        except Exception as exp:

            # Print the exception to the stdio
            print(exp)


# If the function is run as the main file
if __name__ == "__main__":
    # Call the main function
    main()
