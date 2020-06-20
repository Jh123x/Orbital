import socket
import select
import asyncio
import pickle

class Network(object):
    def __init__(self, server:str, port:int):
        """Main network object for connecting to the server"""

        #Creating the socket object
        self.client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Create addr obj
        self.addr = (server, port)

    def connect(self) -> None:
        """Connect to the server"""
        pass

    def send(self, data:object) -> object:
        """Send the data to the server"""
        pass

    def close(self):
        """Close the network port"""
        return self.client.close()


#If this is the main file
if __name__ == '__main__':
    pass

    
