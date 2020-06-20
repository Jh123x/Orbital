import socket
import socketserver
import pickle
import logging
import multiprocessing as mp

#Configure logging format
logging.basicConfig(level=logging.CRITICAL, format = '%(asctime)s - %(levelname)s - %(message)s')

class Player(object):
    def __init__(self, connection):
        """Player object"""
        self.connection = connection

    def recv(self):
        """Receive data from the players"""
        return pickle.loads(self.connection.recv(2048))

    def send(self, data):
        """Send data to the player"""
        return self.connection.sendall(pickle.dumps(data))

class Room(object):
    def __init__(self, player1, player2 = None):
        """Main room object"""

        #Store variables
        self.player1 = player1
        self.player2 = player2

        #Defining the lock 
        self.lock = mp.Lock()

    def __getattribute__(self, name):
        """Method to get different attributes within the Room"""

        #Get the lock
        self.lock.acquire()

        #Proxy to get attribute of object
        def _proxy(*args, **kargs):

            #Get the lock
            self.lock.acquire()

            #Get the attribute from the object
            answer = getattr(self.object, name)(*args, **kargs)

            #Release the lock
            self.lock.release()

            #Return the answer
            return answer

        #Return the function to acquire the attribute
        return _proxy

    def add_player(self, player2) -> None:
        """Add another player"""

        #If player 2 exists
        if self.size() == 2:
            return False

        #Otherwise add the player
        self.player2 = player2
        return True

    def size(self) -> int:
        """Get the size of the room
            At most 2 at least 1
        """
        if self.player1 and self.player2:
           return 2
        elif self.player1 or self.player2:
            return 1
        else:
            return 0

    def start(self) -> None:
        """Start the game for each of the players"""
        pass
    
    def mainloop(self) -> None:
        """Mainloop for the room to run"""
        if player1 and player2:
            pass


class Server(socketserver.ThreadingTCPServer):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    port = 5555
    server = Server(ip,port)
    logging.critical(f"Starting server on: {ip}:{port}")

