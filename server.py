"""
server.py
Kyle Guss

chatroom server
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():  # makes new thread for each client
    while True:
        client, client_address = server.accept()
        print("{0}:{1} has connected".format(client, client_address))
        client.send(bytes("Hello earthling, this is the server", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):      # send chat setup info and receive name, broadcast messages
    name = client.recv(BUFFERSIZE).decode("utf8")
    welcome = ("Welcome {0}! If you ever want to quit, type [quit] to exit.".format(name))
    client.send(bytes(welcome, "utf8"))
    user_joined_message = ("{0} has joined the chat!".format(name))
    broadcast_to_clients(user_joined_message)
    clients[client] = name

    while True:
        raw_msg = client.recv(BUFFERSIZE)
        msg = raw_msg.decode("utf8")
        if "[quit]" in msg:     # safely deletes client
            print("[quit] called")
            client.send(bytes("[quit]", "utf8"))
            client.close()
            del clients[client]
            broadcast_to_clients("{0} has left the chat.".format(name))
            break
        if "[who]" in msg:  # prints list of clients
            print("[who] called")
            constructed_who_message = "[who]: "
            for client in clients:
                constructed_who_message += clients[client] + " "
            client.send(bytes(constructed_who_message, "utf8"))     # send message right back
        else:
            broadcast_to_clients(msg, name)


def broadcast_to_clients(message, user=""):     # send message to all clients
    for sock in clients:
        if user == "":
            sock.send(bytes(message, "utf8"))
        else:
            sock.send(bytes("{0}: {1}".format(user, message), "utf8"))


clients = {}
addresses = {}

# socket info
TCP_IP = "127.0.0.1"
TCP_PORT = 33001
TCP_ADDRESS = (TCP_IP, TCP_PORT)
BUFFERSIZE = 1024

server = socket(AF_INET, SOCK_STREAM)   # init socket
server.bind(TCP_ADDRESS)

if __name__ == "__main__":
    server.listen(5)
    print("Waiting for connection...")
    accept_thread = Thread(target=accept_incoming_connections)
    accept_thread.start()
    accept_thread.join()
    server.close()