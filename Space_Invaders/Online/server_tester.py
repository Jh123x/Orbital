import socket
import pickle

#Creating the socket object
client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Create addr obj
addr = ("195.168.1.215", 5555)

#Connect to the server
client.connect(addr)

print("Connected to server")

while True:
    dat = pickle.loads(client.recv(2048))
    print(f"Received: '{dat}'")
    data = eval(input())
    print(f"Sending: '{data}'")
    client.send(pickle.dumps(data))