import socket
import pickle

class Network(object):
    def __init__(self, server:str, port:int):
        """Main network object for connecting to the server"""

        #Create addr obj
        self.addr = (server, port)

    def send(self, data:object) -> dict:
        """Send data"""
        #Connect to the port and host
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            #Connect to the server
            sock.connect(self.addr)

            # Connect to server and send data
            sock.sendall(pickle.dumps(data))

            # Receive data from the server and shut down
            received = pickle.loads(sock.recv(1024))

        #Return the data
        return received

    def close(self):
        """Close the network port"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            #Connect to the server
            sock.connect(self.addr)

            #Empty byte
            data = b''

            # Connect to server and send data
            sock.sendall(pickle.dumps((self.addr,data)))



#If this is the main file
if __name__ == '__main__':
    network = Network('localhost', 9999, ())

    while True:
        try:
            #Get the input for the data
            data = input("Message: ")

            #Send the data and recv the data
            data = network.send(data)
            print(f'Message sent: {data}')
        except KeyboardInterrupt:
            network.close()
            break
            

    
    

    
