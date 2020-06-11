import socket
import sys
import pickle
import random
import time
import os
from _thread import *

class Server(object):
    def __init__(self, serverip:str, port:int):
        """To initialise the object"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (serverip,port)
        self.id = 0
        self.players = {}
        self.bind()

    def bind(self):
        """Binds to the current addr"""
        try:
            self.socket.bind((server,port))
            self.socket.listen()
            print(f"Server started on {(server,port)}")
        except socket.error as e:
            print(str(e))

    def match_make(self, player):
        """"""
        pass

    def handle_client(self, conn):
        """Handle the client"""
        #Map player to the id
        playerid = self.id
        conn.send(pickle.dumps(playerid))
        self.id += 1

        #Game loop
        while True:

            #Try to receive data from the client
            try:

                #Receive the data
                data = conn.recv(1024)

                #If it is empty client disconnected
                if not data:
                    print("Client disconnected")
                    break

                #Otherwise process the data
                else:
                    #Unpickle the data
                    data = pickle.loads(data)
                    print(f"Received: {data}")

                    #If data is askinf for random str
                    if data[0] == 'rand':
                        reply = random.randint(0,60*50)

                    #If data is player data
                    elif len(data) == 3:
                        reply = list([data[0], list(data[1]), data[2]])
                        reply[1][1] = 60
                        reply = tuple(reply)

                conn.sendall(pickle.dumps(reply))
                print(f"Sent: {reply}")
            
            except socket.error as exp:
                print(exp)
                break

                #Close the connection
        print("Lost connection")
        conn.close()
        sys.exit()
        

    def mainloop(self):
        #The main loop for the server
        while True:

            conn, addr = self.socket.accept()

            print(f"{addr} connected")

            start_new_thread(self.handle_client, (conn,))

            # time.sleep(0.1)



#Define variables and port
server = '192.168.1.215'
port = 5555

server=  Server(server,port)
server.mainloop()