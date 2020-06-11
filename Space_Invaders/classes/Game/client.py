import socket
import pickle

class Network(object):
    def __init__(self, server:str, port:int):
        """Main network object for connecting to the server"""

        #Creating the socket object
        self.client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Create addr obj
        self.addr = (server, port)

        #Connect to the server and get an ID
        self.id = self.connect()

    def get_id(self):
        """Get current position of the client"""
        return self.id

    def connect(self):
        """Connect to the server"""
        try:
            #Connect to the server
            self.client.connect(self.addr)

            #Return the id that the server received
            return pickle.loads(self.client.recv(2048))
        except socket.error:
            print("Error network")


    def send(self, data:object) -> None:
        """Send the data to the server"""
        try:
            self.client.send(pickle.dumps(data))

            data = pickle.loads(self.client.recv(2048))
            print(f"Data sent: {data}")
            return data
        except socket.error as exp:
            print(exp)



if __name__ == '__main__':
    #Define variables and port
    server = '192.168.1.215'
    port = 5555
    client = Network(server, port)
    print(client.send("Hello"))
    print(client.send("World"))
    
