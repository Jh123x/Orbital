import socket
import sys
import pickle
import random
import queue
import logging
from _thread import *

logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.DEBUG)

class CheckableQueue(queue.Queue): # or OrderedSetQueue
    def __contains__(self, item):
        with self.mutex:
            return item in self.queue

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
        self.data = (id, 300, False)

    def get_addr(self) -> tuple:
        """Get address"""
        return self.addr

    def get_id(self):
        """Get the id of the player"""
        return self.id

    def get_conn(self):
        """Get the connection socket"""
        return self.conn

    def __eq__(self, other):
        return self.addr == self.addr

    def __hash__(self):
        return hash(self.addr)

    def recv(self):
        """Receive data from the socket"""
        try:
            data = self.get_conn().recv(2048)
        except socket.error as exp:
            logging.debug(exp)
            self.active = False
            return None
        if data:
            return pickle.loads(data)
        else:
            return data

    def send(self, data):
        """Send the data to the socket"""
        self.conn.sendall(pickle.dumps(data))

    def set_data(self, data):
        """Set the current client data to data"""
        self.data = data

    def is_active(self):
        """Check if it is active"""
        return self.active

    def get_data(self):
        """Get the current client data"""
        return self.data

    def close(self):
        """Close the connection"""
        self.conn.close()

    def __repr__(self):
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
        if command == 'waiting':
            return False
        else:
            assert False, f"Invalid command {command}"

    def update_data(self, client, data):
        """Update the data"""
        logging.debug(f'received: {data}')
        if type(data) == str:
            client.send(self.parse_command(data))
        else:
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
            self.c1.send(self.c2.get_data()+(rand,True))
            self.c2.send(self.c1.get_data()+(rand,False))

        #Exit the thread
        sys.exit()
            
    def mainloop(self):
        """Handle the threads"""
        self.handle_clients()

    def is_active(self):
        """Check if the player is active"""
        return self.active

class Server(object):
    def __init__(self, serverip:str, port:int):
        """To initialise the object"""

        #Create the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Store the addr
        self.addr = (serverip,port)

        #Initialize id
        self.id = 0
        self.max = 1000

        #Create player queue
        self.players = CheckableQueue()
        self.removed = set()

        #Bind to the port
        self.bind()

        #Variable to check if a thread is delicated to updating players
        self.update_thread = False

    def bind(self):
        """Binds to the current addr"""
        #Try to bind to the socket
        try:

            #Bind to that server and port
            self.socket.bind((server,port))

            #Listen to the port
            self.socket.listen()

            #Print out the Server started
            logging.critical(f"Server started on {(server,port)}")

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

                #Exit the thread
                sys.exit()

            #Try to receive data from the client
            try:

                #Receive the data
                data = client.recv()

                #If it is empty client disconnected
                if len(data) == 0 or client.is_active():
                    if not data:
                        client.close()
                        if client in self.players:
                            self.removed.add(client)
                    logging.critical(f"Client disconnected\n{client}\nqsize: {self.players.qsize()}\ndata: {data}")
                    sys.exit()

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
            self.players.put_nowait(player)

            #Handle the player
            start_new_thread(self.handle_client, (player,))

    def update(self):
        """Update the lists"""
        while True:
            #Get the next 2 players
            player1 = self.get_next_player()
            player2 = self.get_next_player()

            if player1 and player2:
                #Matchmake the players
                self.matchmake(player1, player2)

            elif player1 and player1 not in self.players:
                self.players.add(player1)

            elif player2 and player2 not in self.players:
                self.players.add(player2)

            else:
                assert False, "Not suppose to hit here"

    def get_next_player(self):
        """Get the next player in the queue"""

        #Get the next player in queue
        player = self.players.get()

        #Keep getting the next player while they are in the set
        while player in self.removed:

            #Remove it from the removed set
            logging.debug(f"Removed: {player}")
            self.removed.remove(player)

            #If player is non-empty
            if not self.players.empty():
                #Get the next player
                player = self.players.get()

            else:
                #Return None as there is no players left
                return False

        #Return a player that is not in the set
        return player


    def matchmake(self, player1, player2):
        """Matchmake the players"""
        #While there are 2 or more clients
        while self.players.qsize() >= 2:

            logging.debug(f"Matched: \n{player1}\n{player2}")

            #Add client handlers to handler object
            chandle = Client_handler(player1,player2)

            #Start the game in separate thread
            start_new_thread(chandle.mainloop, ())


#If this is run as the main function
if __name__ == "__main__":
    #Define variables and port
    server = '192.168.1.215'
    port = 5555
    server=  Server(server,port)
    server.mainloop()