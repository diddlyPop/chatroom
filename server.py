"""
server.py
Kyle Guss

chatroom server
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# socket info
TCP_IP = "167.71.156.224"
LOCAL_IP = "127.0.0.1"
TCP_PORT = 33001
TCP_ADDRESS = (LOCAL_IP, TCP_PORT)
AUTH_TOKEN = "1111"
BUFFERSIZE = 1024


class Server:

    def __init__(self):
        self.names = []
        self.clients = {}
        self.addresses = {}
        self.commands = ["/help", "/who", "/quit"]
        self.server = socket(AF_INET, SOCK_STREAM)   # init socket
        self.server.bind(TCP_ADDRESS)
        self.server.listen(5)
        print("Waiting for connection...")
        self.accept_thread = Thread(target=self.accept_incoming_connections)
        self.accept_thread.start()
        self.accept_thread.join()
        self.server.close()

    def accept_incoming_connections(self):  # makes new thread for each client
        while True:
            client, client_address = self.server.accept()
            print("{0}:{1} has connected".format(client, client_address))
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):  # send chat setup info and receive name, broadcast messages
        login = client.recv(BUFFERSIZE).decode("utf8")
        name, token = login.split('-')
        while name in self.names or AUTH_TOKEN not in token:
            client.send(bytes("DENY", "utf8"))
            login = client.recv(BUFFERSIZE).decode("utf8")
            name, token = login.split('-')
        client.send(bytes("ACCEPT", "utf8"))
        self.names.append(name)

        user_joined_message = ("{0} has joined the chat!".format(name))
        self.broadcast_to_clients(user_joined_message)
        self.clients[client] = name

        while True:
            try:
                msg = client.recv(BUFFERSIZE).decode("utf8")
            except OSError:  # client left
                break
            if "/quit" in msg:  # safely deletes client
                client.close()
                del self.clients[client]
                self.names.remove(name)
                self.broadcast_to_clients("{0} has left the chat.".format(name))
                break
            elif "/who" in msg:  # prints list of clients
                print("/who called")
                client.send(bytes(str(self.names), "utf8"))  # send message right back
            elif "/help" in msg:
                print("help called")
                client.send(bytes(str(self.commands), "utf8"))  # send message right back
            elif len(msg) > 100:
                print("message size too big")
                client.send(bytes("Message too large", "utf8"))  # send message right back
            else:
                self.broadcast_to_clients(msg, name)

    def broadcast_to_clients(self, message, user=""):  # send message to all clients
        try:
            clients_copy = self.clients
            for sock in clients_copy:
                try:
                    if user == "":
                        sock.send(bytes(message, "utf8"))
                    else:
                        sock.send(bytes("{0}: {1}".format(user, message), "utf8"))
                except Exception as e:
                    del self.clients[sock]
                    pass
        except Exception as e:
            print(e)


if __name__ == "__main__":
    S = Server()
