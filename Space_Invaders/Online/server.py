import socket
import sys
import pickle
import random
import queue
import logging
from _thread import *

logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)

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
        return f"Client:\nAddr: {self.addr}\nActive: {self.is_active()}\nID:{self.id}"

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
            while int(rand*10) == 5:
                rand = random.random()

            data1 = self.c1.recv()
            data2 = self.c2.recv()

            if len(data1) == 0 or len(data2) == 0:
                self.c1.close()
                self.c2.close()
                break
            
            self.update_data(self.c1,data1)
            self.update_data(self.c2,data2)
            self.c1.send(self.c2.get_data()+(rand,1-rand))
            self.c2.send(self.c1.get_data()+(rand,rand))

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
        self.bind()
        self.update_thread = False

    def bind(self):
        """Binds to the current addr"""
        try:
            self.socket.bind((server,port))
            self.socket.listen()
            logging.debug(f"Server started on {(server,port)}")
        except socket.error as e:
            logging.debug(str(e))

    def handle_client(self, client:Client):
        """Handle the client"""
        #Map player to the id
        client.send(client.get_id())

        #Game loop
        while True:

            if client.is_active():
                logging.debug(f"{client.get_addr()}: Active")
                #Exit the thread
                sys.exit()

            #Try to receive data from the client
            try:

                #Receive the data
                data = client.recv()

                #If it is empty client disconnected
                if client not in self.players:
                    logging.debug(f"Client disconnected\n{client}")
                    sys.exit()

                #Otherwise process the data
                else:
                    #Unpickle the data
                    logging.debug(f"{client.get_addr()}Received: {data}")

                    #If data is asking for random str
                    if data == 'waiting':
                        reply = True

                    client.send(reply)
                    logging.debug(f"Sent: {reply}")
            
            except socket.error as exp:
                logging.debug(exp)
                break

    def mainloop(self):
        #The main loop for the server
        while True:
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

            #Add the client to the list of players
            self.players.put(player)

            #Handle the player
            start_new_thread(self.handle_client, (player,))

    def update(self):
        """Update the lists"""
        while True:
            #Increment the id if it is greater than a large number
            if self.id == self.max:
                self.id = 0
            else:
                self.id += 1

            #Matchmake
            self.matchmake()


    def matchmake(self):
        """Matchmake the players"""
        #While there are 2 or more clients
        while self.players.qsize() >= 2:

            logging.debug("Matched")

            #Get the next 2 players
            player1 = self.players.get()
            player2 = self.players.get()

            #Add client handlers to handler object
            chandle = Client_handler(player1,player2)

            #Start the game in separate thread
            start_new_thread(chandle.mainloop, ())




#Define variables and port
server = '192.168.1.215'
port = 5555
server=  Server(server,port)
server.mainloop()