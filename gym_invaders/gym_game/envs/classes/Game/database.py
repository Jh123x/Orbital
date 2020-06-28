#To manage the database
import sqlite3

class ScoreBoard(object):
    def __init__(self, dbpath:str, max_length:int = 5):
        """Class for keeping track of the high score
            Arguments:
                dbpath: A string containing the path to the database (string)
                max_length: An integer containing the max length to keep track of (int): default = 5
            
            Methods:
                execute: Execute a particular string in sql
                remove: Remove a name from the scoreboard
                remove_exact: Remove the exact copy of the name and score from the scoreboard
                add: Add the name and score to the scoreboard
                add_all: Add all items passed into the scoreboard
                remove_all: Remove all names,score pairs that are provided
                fetch_all: Fetch all the data in database
                is_cache: Check if the database data is stored in cache
        
        """

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
        """Execute the command in the form of a string
            Arguments:  
                command: a string containing the sql command (string)
                *args: The arguments to the placed within the command wildcards if any (tuple)
            Returns:
                No return
        """

        #Run the command
        self.cursor.execute(command, *args)

        #Execute the command through the connection
        self.connection.commit()
    
    def remove(self, name:str) -> None:
        """Remove the last entry from the highscore board
            Arguments:
                name: Name of the entry to be removed (string)
            Returns:
                No return
        """
        #Remove from the database where the name matches the name to be removed
        self.execute("DELETE FROM highscore WHERE name = ?", (name,))

        #Mark the database as changed
        self.changed = True

    def remove_exact(self, name:str, score:int) -> None:
        """Removes the entry that matches both the name and the highscore
            Arguments:
                name: Name of the entry to be removed (string)
                score: Score of the entry to be removed (int)
            Returns:
                There is no return
        """

        #Remove the entry from the database
        self.execute("DELETE FROM highscore WHERE name = ? AND score = ?", (name, score))

        #Mark the database as changed
        self.changed = True

    def add(self, name:str, score:int) -> None:
        """Add a name and a score to the scoreboard
            Arguments:
                name: Name of the person to be inserted (string)
                score: Score of the person to be inserted (int)
            Returns: 
                Does not return 
        """
        #Insert the element into the table
        self.execute('INSERT INTO highscore VALUES(NULL, ?, ?)', (name,score))

        #Execute the command TODO(Test if this is needed)
        self.connection.commit()

        #Mark the database as changed
        self.changed = True

    def add_all(self, *args) -> None:
        """Add all the items into the database
            Arguments: 
                *args: list of items to be added to the database (List of tuples)
            Returns: 
                No return
        """
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
        """Remove all the items from the table
            Arguments:
                *args: list of items to be removed from the database (list of tuples)
            Returns:
                No return
        """
        #Call the cache
        if not self.is_cache():
            self.fetch_all()

        #For each of the items
        for item in args:

            #If the item is in the cache remove it
            if item in self.cache:
                self.remove_exact(item[1], item[2])
        
    def fetch_all(self) -> tuple:
        """Fetch all the data from the highscore table
            Arguments:
                No arguments
            Returns: 
                A tuple containing all the entries in the highscore table (tuple of tuple)
        """
        
        #If there is no cache or if there are changes in the cache
        if self.changed or not self.is_cache():
            
            #Fetch all the items in the table and add it to the cache
            self.cursor.execute("SELECT * FROM highscore")
            self.cache = self.cursor.fetchall()

            #Make the changes as none
            self.changed = False

        #Return the items
        return self.cache

    def is_cache(self) -> bool:
        """Check if there is a cached copy
            Arguments: 
                No arguments
            Returns:
                Returns a boolean to indicate if there is a cache (bool)
        """
        return True if self.cache else False

    def __del__(self):
        """Destructor for the Scoreboard
            Arguments:
                No Arguments
            Returns:
                Does not return
        """
        self.connection.close()

    
def main() -> None:
    """The main function for the database class used for testing
        Arguments:
            No arguments
        Returns: 
            No returns
    """
    #Create the scoreboard database
    db = ScoreBoard("../../data/test.db")

    #For debugging
    print(f"Running the main function from database file")
    print(f"Scoreboard db created")

    

    #Create a while loop for the user to test commands as they are typed into the terminal
    while(True):
        #Print entries
        print(db.fetch_all())
        try:
            command = input("Type in the command: ").strip()
            if command == 'q':
                break
            print(eval(command))
        except Exception as exp:
            print(exp)


#If the function is run as the main file call the main function
if __name__ == "__main__":
    main()