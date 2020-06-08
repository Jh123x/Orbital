import socket
import multiprocessing as mp

#Define variables and port
server = ''
port = 5555

#Wrapper function for multithreading
def wrapper():
    async def func(f,*args):
        return f(*args)
    return func

#Function to entertain the threaded clients
def handle_client(connection):
    """Function to handle each of the connected clients"""
    
    while True:
        try: 
            #Try to receive data from the client
            data = conn.recv(1024)

            #Decode the data to utf-8
            reply = data.decode('utf-8')

class Server(object):
    def __init__(self, servername:str, port:int):
        """The main server object"""

        #Create a list to store the clients
        self.clients = []

        #Create a server socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Bind the server to the port
        try:
            #Binds to the port
            self.socket.bind((servername,port))
        except socket.error as e:

            print(f"Socket error: {e}")
            return

        #Listen to the port
        s.listen(5)

    def mainloop(self):
        """Mainloop for the server"""
        while True:

            #Accept the incoming packet
            conn, addr = s.accept()
            print(f"Device: {addr} connected")

            #Handle the client in a new thread
            mp.start_new_thread(threaded_client, (conn,))

            

def main() -> None:
    """The main function for the game"""
    pass


#If this script is executed as the main script
if __name__ == '__main__':
    main()