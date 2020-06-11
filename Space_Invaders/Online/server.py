import socket
import sys
import pickle
import random
import time
import os
from _thread import *

class Client(object):
    def __init__(self, conn, id:int):
        """Initialiser for the Client"""

        #Store variables
        self.conn = conn
        self.id = id
        self.active = False

        #Set default data
        self.data = (id, 300, False)

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
        except:
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
        return self.active

    def get_data(self):
        """Get the current client data"""
        return self.data

    def close(self):
        """Close the connection"""
        self.conn.close()

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
        self.rand = random.randint(0,300)

    def handle_client(self, client:Client):
        """Handle the client"""
        #Game loop
        while True:
            try:
                data = client.recv()
            except EOFError:
                client.close()
                return
            
            if data == 'rand':
                return self.random

            elif data == 'waiting':
                return False
            
            else:
                if self.c1 == client:
                    client.send(c2.get_data())
                else:
                    client.send(c1.get_data())
            
    def mainloop(self):
        """Handle the threads"""

        #Start new thread to handle client 1
        start_new_thread(self.handle_client,(self.c1,))

        #Handle client 2
        self.handle_client(self.c2)

    def is_active(self):
        """Check if the player is active"""
        return self.active

class Server(object):
    def __init__(self, serverip:str, port:int):
        """To initialise the object"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (serverip,port)
        self.id = 0
        self.max = 1000
        self.players = []
        self.handlers = []
        self.bind()

    def bind(self):
        """Binds to the current addr"""
        try:
            self.socket.bind((server,port))
            self.socket.listen()
            print(f"Server started on {(server,port)}")
        except socket.error as e:
            print(str(e))

    def handle_client(self, client):
        """Handle the client"""
        #Map player to the id
        client.send(client.get_id())

        #Game loop
        while not client.is_active():

            #Try to receive data from the client
            try:

                #Receive the data
                data = client.recv()

                #If it is empty client disconnected
                if not data:
                    print("Client disconnected")
                    break

                #Otherwise process the data
                else:
                    #Unpickle the data
                    print(f"Received: {data}")

                    #If data is askinf for random str
                    if data == 'waiting':
                        reply = True

                client.send(reply)
                print(f"Sent: {reply}")
            
            except socket.error as exp:
                print(exp)
                break

        #Exit the thread
        sys.exit()
        

    def mainloop(self):
        #The main loop for the server
        while True:

            #Accept the connection
            conn, addr = self.socket.accept()

            #Print the connected message
            print(f"{addr} connected")

            #Add the client to the list of players
            self.players.append(Client(conn, self.id))

            #Handle the last player
            start_new_thread(self.handle_client, (self.players[-1],))

            #Filter out all inactive handlers
            self.handlers = list(filter(lambda x: x.is_active(), self.handlers))

            #Filter out all inactive players
            self.players = list(filter(lambda x: x.is_active(), self.handlers))

            #Increment the id if it is greater than a large number
            if self.id == self.max:
                self.id = 0
            else:
                self.id += 1

            #While there are 2 or more clients
            while len(self.players) >= 2:
                
                #Add client handlers to handler object
                self.handlers.append(Client_handler(self.players.pop(),self.players.pop()))

                #Start the game in separate thread
                start_new_thread(self.handlers[-1].mainloop(), ())




#Define variables and port
server = '192.168.1.215'
port = 5555

server=  Server(server,port)
server.mainloop()