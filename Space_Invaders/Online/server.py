import socket
import sys
import pickle
import random
import logging
from multiprocessing import *
from CheckableQueue import CheckableQueue

#Setting the configuration for logging
logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.DEBUG)

def start_new_thread(function,args):
    """Start a new thread"""
    p = Process(target = function, args = args)
    p.start()
    

class Client(object):
    def __init__(self, conn, id:int, addr:tuple):
        """Initialiser for the Client"""

        #Store variables
        self.conn = conn
        self.id = id
        self.active = False
        self.closed = False
        self.addr = addr

        #Set default data
        self.data = (id, 300, False, 0)

    def get_addr(self) -> tuple:
        """Get address"""
        return self.addr

    def get_id(self) -> int:
        """Get the id of the player"""
        return self.id

    def get_conn(self):
        """Get the connection socket"""
        return self.conn

    def __eq__(self, other:object) -> bool:
        """Check for equality"""
        if type(self) == type(other):
            return self.get_addr() == other.get_addr()
        return False

    def recv(self):
        """Receive data from the socket"""

        #Try receiving the data
        try:
            data = self.get_conn().recv(2048)

        #If there is an error return None
        except socket.error as exp:
            logging.debug(exp)
            return b""

        #If data is not empty
        if data:

            #Pickle the data
            return pickle.loads(data)
        
        #Otherwise return empty data
        else:
            return data

    def send(self, data) -> None:
        """Send the data to the socket"""
        self.conn.sendall(pickle.dumps(data))

    def set_data(self, data) -> None:
        """Set the current client data to data"""
        self.data = data

    def is_active(self) -> bool:
        """Check if it is active"""
        return self.active

    def get_data(self):
        """Get the current client data"""
        return self.data

    def close(self) -> None:
        """Close the connection"""
        self.conn.close()
        self.closed = True

    def __repr__(self) -> str:
        """Representation of client when printed"""
        return f"Client:Addr: {self.addr} Active: {self.is_active()}"

class Client_handler(object):
    def __init__(self, client1:Client, client2:Client):
        """Class for handling interaction between 2 clients"""
        
        #Store the variables
        self.c1 = client1
        self.c2 = client2

        #Activate both the clients
        self.c1.active = True
        self.c2.active = True

        #Mark active as true
        self.active = True

        #Generate first random number
        self.random = random.random()

    def parse_command(self, command):
        """Parse commands"""

        #If command is waiting
        if command == 'waiting':

            #Return False as clients in the client handler is not waiting
            return False

        #Otherwise
        else:
            
            #Assert an error
            assert False, f"Invalid command {command}"

    def update_data(self, client, data):
        """Update the data"""
        logging.debug(f'received: {data}')

        #If the datatype is string
        if type(data) == str:

            #Parse the command and send back the reply
            client.send(self.parse_command(data))

        #Otherwise it is player data
        else:

            #Update the data of the player
            client.set_data(data)

    def handle_clients(self):
        """Handle the clients"""
        #Game loop
        while True:

            #Generate first random number
            rand = random.random()

            #Reroll if integer is 5
            while int(rand*10) == 5:
                #Generate random number
                rand = random.random()

            #Receive data from both the clients
            data1 = self.c1.recv()
            data2 = self.c2.recv()

            #Check if any of them disconnected
            if not data1 or not data2:

                #Close the sockets for both of them
                self.c1.close()
                self.c2.close()
                
                #Break out of the loop
                break
            
            #Update the data of the clients
            self.update_data(self.c1,data1)
            self.update_data(self.c2,data2)

            #Send the data to the clients
            c1_data = self.c2.get_data()+(rand,True)
            c2_data = self.c1.get_data()+(rand,False)
            self.c1.send(c1_data)
            self.c2.send(c2_data)

        #Exit the thread
        exit()

    def is_active(self):
        """Check if the player is active"""
        return self.active

class Server(object):
    players = CheckableQueue()
    removed = []
    def __init__(self, serverip:str, port:int):
        """To initialise the object"""

        #Create the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Store the addr
        self.addr = (serverip,port)

        #Initialize id
        self.id = 0
        self.max = 1000

        #Bind to the port
        self.bind()

        #Variable to check if a thread is delicated to updating players
        self.update_thread = False

    def bind(self):
        """Binds to the current addr"""
        #Try to bind to the socket
        try:

            #Bind to that server and port
            self.socket.bind(self.addr)

            #Listen to the port
            self.socket.listen()

            #Print out the Server started
            logging.critical(f"Server started on {self.addr}")

        #If there was an error
        except socket.error as e:

            #Log the error
            logging.debug(f"Connection error: {str(e)}")

    def handle_client(self, client:Client):
        """Handle the client"""
        #Map player to the id
        client.send(client.get_id())

        #Game loop
        while True:

            #If client is active, 
            if client.is_active():

                #Check if the client is active
                logging.debug(f"{client.get_addr()}: Active")
                break


            #Try to receive data from the client
            try:

                #Receive the data
                data = client.recv()

                #If the data is empty
                if not data:
                    logging.critical(f"Client disconnected\n{client}\nqsize: {Server.players.qsize()}\ndata: {data}\nQueue: {Server.removed}")
                    client.close()
                    Server.removed.append(client)
                    
                    #Break out of the loop
                    break

                #Otherwise process the data
                else:
                    #Unpickle the data
                    logging.debug(f"{client.get_addr()}Received: {data}")

                    #If data is asking for random str
                    if data == 'waiting':
                        reply = True
                    else:
                        assert False, f"Error msg: {data}"

                    client.send(reply)
                    logging.debug(f"Sent: {reply}")
            
            #If there is a connection error
            except socket.error as exp:

                #Log the bug
                logging.debug(exp)

                #Break out of the loop
                break

        exit()

    def mainloop(self):
        #The main loop for the server
        while True:

            #If the update thread has nt started
            if not self.update_thread:

                #Update the list
                start_new_thread(self.update, ())
                self.update_thread = True

            #Accept the connection
            conn, addr = self.socket.accept()

            #Print the connected message
            logging.debug(f"{addr} connected")

            #Create player var
            player = Client(conn, self.id,addr)

            #Increment the id for the next player
            if self.id < self.max:
                self.id += 1
            else:
                self.id = 0

            #Add the client to the list of players
            Server.players.put_nowait(player)

            #Handle the player
            start_new_thread(self.handle_client, (player,))

    def update(self):
        """Update the lists"""
        while True:
            if Server.players.qsize() >= 2:

                #Get the next 2 players
                player1 = self.get_next_player()
                player2 = self.get_next_player()

                if player1 and player2:
                    #Matchmake the players
                    logging.debug(f"Player matched")
                    self.matchmake(player1, player2)

                elif player1:
                    logging.debug(f"Added player 1 back to queue")
                    Server.players.add(player1)

                elif player2:
                    logging.debug(f"Added player 2 back to queue")
                    Server.players.add(player2)

                else:
                    assert False, "Not suppose to hit here"

    def get_next_player(self):
        """Get the next player in the queue"""

        #Get the next player in queue
        player = Server.players.get()

        logging.debug(f"Removed queue: {Server.removed}")
        logging.debug(f"{player} in queue: {player in Server.removed}")

        #Keep getting the next player while they are in the set
        while player in Server.removed:

            #Remove it from the removed set
            logging.debug(f"Removed: {player}")
            Server.removed.remove(player)

            #If player is non-empty
            if not Server.players.empty():

                #Get the next player
                player = Server.players.get()

            else:
                #Return None as there is no players left
                return False

        #Return a player that is not in the set
        return player


    def matchmake(self, player1, player2):
        """Matchmake the players"""
        logging.debug(f"Matched: {player1} and {player2}")

        #Add client handlers to handler object
        chandle = Client_handler(player1,player2)

        #Start the game in separate thread
        start_new_thread(chandle.handle_clients, ())

def main():
    #Define variables and port
    serverip = '192.168.1.215'
    port = 5555
    server =  Server(serverip,port)
    server.mainloop()


#If this is run as the main function
if __name__ == "__main__":
    main()
    # client1 = Client(None, 1, ('192.168.1.1',1234))
    # client2 = Client(None, 1, ('192.168.1.1',1234))
    # print(client1 == client2)

