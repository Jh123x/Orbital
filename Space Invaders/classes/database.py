import sqlite3

class ScoreBoard(object):
    def __init__(self, dbpath:str, max_length:int = 10):
        """Class for keeping track of the high score"""

        #Store the database path
        self.dbpath = dbpath

        #Set the max number of highscore to be stored for the players
        self.max_length = max_length

        #Connect to the database
        self.connection = sqlite3.connect(dbpath)

        #Get the cursor of the database
        self.cursor = self.connection.cursor()

        #Cache
        self.cache = []
        self.changed = True


        #Create the table if it does not exist
        self.execute("CREATE TABLE IF NOT EXISTS highscore (id INTEGER, name TEXT, score INTEGER)")

    def execute(self, command:str, *args) -> None:
        """Execute the command in the form of a string"""

        #Run the command
        self.cursor.execute(command, *args)

        #Execute the command through the connection
        self.connection.commit()
    
    def remove(self, name:str) -> None:
        """Remove the last entry from the highscore board"""
        self.execute("DELETE FROM highscore WHERE name = ?", (name,))
        self.changed = True

    def remove_exact(self, name:str, score:int) -> None:
        self.execute("DELETE FROM highscore WHERE name = ? AND score = ?", (name, score))
        self.changed = True

    def add(self, name:str, score:int):
        #Insert the element into the table
        self.execute('INSERT INTO highscore VALUES(NULL, ?, ?)', (name,score))
        self.connection.commit()
        self.changed = True

    def add_all(self, *args):
        """Add all the items into the database"""
        #Call the cache
        if not self.is_cache():
            self.fetch_all()

        for item in args:
            if item not in self.cache:
                self.add(item[1],item[2])
                self.cache.append(item)

    def remove_all(self, *args):
        """Remove all the items from the table"""
        #Call the cache
        if not self.is_cache():
            self.fetch_all()

        for item in args:
            if item in self.cache:
                self.remove_exact(item[1], item[2])
        
    def fetch_all(self) -> tuple:
        """Fetch all the data from the highscore table"""
        if not self.is_cache():
            self.cursor.execute("SELECT * FROM highscore")
            self.cache = self.cursor.fetchall()
            self.changed = False
        return self.cache

    def is_cache(self) -> bool:
        """Check if there is a cached copy"""
        return self.cache

    def __del__(self):
        """Destructor for the Scoreboard"""
        self.connection.close()

    
def main() -> None:
    """The main function for the database class used for testing"""
    db = ScoreBoard("../data/test.db")
    print(f"Scoreboard db created")
    while(True):
        try:
            print(eval(input("Type in the command: ").strip()))
        except Exception as exp:
            print(exp)


if __name__ == "__main__":
    main()