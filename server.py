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
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):      # send chat setup info and receive name, broadcast messages
    login = client.recv(BUFFERSIZE).decode("utf8")
    name, token = login.split('-')
    while name in names or AUTH_TOKEN not in token:
        client.send(bytes("DENY", "utf8"))
        login = client.recv(BUFFERSIZE).decode("utf8")
        name, token = login.split('-')
    client.send(bytes("ACCEPT", "utf8"))
    names.append(name)

    user_joined_message = ("{0} has joined the chat!".format(name))
    broadcast_to_clients(user_joined_message)
    clients[client] = name

    while True:
        try:
            msg = client.recv(BUFFERSIZE).decode("utf8")
        except OSError:  # client left
            break
        if "/quit" in msg:     # safely deletes client
            client.close()
            del clients[client]
            names.remove(name)
            broadcast_to_clients("{0} has left the chat.".format(name))
            break
        elif "/who" in msg:  # prints list of clients
            print("/who called")
            client.send(bytes(str(names), "utf8"))     # send message right back
        elif "/help" in msg:
            print("help called")
            client.send(bytes(str(commands), "utf8"))  # send message right back
        elif len(msg) > 100:
            print("message size too big")
            client.send(bytes("Message too large", "utf8"))  # send message right back
        else:
            broadcast_to_clients(msg, name)


def broadcast_to_clients(message, user=""):     # send message to all clients
    try:
        clients_copy = clients
        for sock in clients_copy:
            try:
                if user == "":
                    sock.send(bytes(message, "utf8"))
                else:
                    sock.send(bytes("{0}: {1}".format(user, message), "utf8"))
            except Exception as e:
                del clients[sock]
                pass
    except Exception as e:
        print(e)


names = []
clients = {}
addresses = {}
commands = ["/help", "/who", "/quit"]
# socket info
TCP_IP = "167.71.156.224"
LOCAL_IP = "127.0.0.1"
TCP_PORT = 33001
TCP_ADDRESS = (TCP_IP, TCP_PORT)
AUTH_TOKEN = "1111"
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
