import socket
import pickle

class Network(object):
    def __init__(self, server:str, port:int):
        """Main network object for connecting to the server"""

        #Creating the socket object
        self.client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Create addr obj
        self.addr = (server, port)

        #Keep track of the number of tries
        self.tries = 0

        #Connect to the server and get an ID
        self.id = self.connect()

    def get_id(self):
        """Get current position of the client"""
        return self.id

    def connect(self):
        """Connect to the server"""
        try:
            #Add to number of tries
            self.tries += 1

            #Connect to the server
            self.client.connect(self.addr)

            #Reset the tries
            self.tries = 0

            #Return the id that the server received
            return pickle.loads(self.client.recv(2048))
        
        #If there is an error
        except socket.error:
            print("Error network")

            #Try connecting again
            if self.tries < 10:
                self.connect()


    def send(self, data:object) -> None:
        """Send the data to the server"""
        try:
            #Add to tries
            self.tries += 1

            #Send the data over to the server
            self.client.send(pickle.dumps(data))

            #Get the data from the server
            data = self.client.recv(2048)

            if data:
                data = pickle.loads(data)

            #Reset the tries
            self.tries = 0

            #Return the data
            return data

        #If there is error print the error and try again
        except socket.error as exp:
            print(exp)
            if self.tries < 10:
                return self.send(data)

    def close(self):
        """Close the network port"""
        return self.client.close()

    
