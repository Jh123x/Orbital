import socketserver
import logging
import pickle
import random

#Configure logging format
logging.basicConfig(level=logging.CRITICAL, format = '%(asctime)s - %(levelname)s - %(message)s')

class Request_Handle(socketserver.BaseRequestHandler):
    player = {}
    first = set()
    pair = {}
    waiting_list = set()
    random = random.random()

    @staticmethod
    def remove_from_all(player):
        """Remove player from all vars"""
        # partner = Request_Handle.player[player]
        del Request_Handle.player[player]
        del Request_Handle.pair[player]
        Request_Handle.first.remove(player)
        Request_Handle.waiting_list.remove(player)
        

    def handle(self):
        """Method to handle the client"""

        #Main loop to handle the client
        data = pickle.loads(self.request.recv(2048))
        player = self.client_address[0]

        #Get id of the player
        logging.critical(f"{self.client_address[0]} wrote: {data}")

        #If data is empty
        if not data:

            #Remove the players
            Request_Handle.remove_from_all(player)
            return

        #If player is new player
        if player not in Request_Handle.player:

            #Check if there is anyone waiting
            if len(Request_Handle.waiting_list) > 0:

                #Get the first player and remove from the list
                partner = Request_Handle.waiting_list.pop()

                #Form the players as pairs
                Request_Handle.pair[partner] = player
                Request_Handle.pair[player] = partner

            #Otherwise
            else:

                #Add the player to the waiting list
                Request_Handle.waiting_list.add(player)
                Request_Handle.first.add(player)

        #Place data into dict
        Request_Handle.player[player] = data

        #If player is not waiting send his partner data over
        if player not in Request_Handle.waiting_list:

            #Get the partner
            partner = Request_Handle.pair[player]

            #If the data is blank
            if not Request_Handle.player[partner]:

                #Remove player
                msg = {'disconnected': True}

            else:
                #Send the partner data  
                msg = {'data':Request_Handle.player[partner],
                        'waiting':False,
                        'seed':Request_Handle.random,
                        'isfirst': player in Request_Handle.first,
                        'disconnected': False}

        #Otherwise
        else:
            msg = {'waiting':True}

        #Send the msg
        self.request.sendall(pickle.dumps(msg))
        

class Server(socketserver.ThreadingTCPServer):
    def __init__(self, address, request_handle):
        super().__init__(address, request_handle)

if __name__ == '__main__':
    ip = '192.168.1.215'
    port = 9999
    server = Server((ip,port), Request_Handle)
    logging.critical(f"Starting server on: {ip}:{port}")
    server.serve_forever()
    

