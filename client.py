import PySimpleGUI as simpleg
import socket, os
from threading import Thread


def launch_login():     # displays login prompt and returns user login
    layout = [
        [simpleg.Text('Please choose a username to chat under.')],
        [simpleg.Text('Username: ', size=(15, 1)), simpleg.InputText('')],
        [simpleg.Submit(), simpleg.Cancel()]
    ]
    window = simpleg.Window('Login').Layout(layout)
    event, values = window.Read()
    user = values[0]
    window.close()
    return user


def launch_chatbox(user):   # displays chatbox with custom user from login, calls send_message
    layout = [
        [simpleg.Output(size=(80, 20), background_color="black", text_color="white")],
        [simpleg.Text('%s: ' % user, size=(15, 1)), simpleg.InputText('', do_not_clear=False)],
        [simpleg.Submit('Send'), simpleg.Cancel()]
    ]
    window = simpleg.Window('Chat').Layout(layout)
    while True:
        event, values = window.Read()
        if event in (None, 'Cancel'):
            break
        else:
            send_message(values[0])   # event sends out message from our client with details
    window.Close()


def send_message(message_to_send):    # send_message transmits client username and message
    connection.send(bytes(message_to_send, "utf8"))
    print("sending: " + message_to_send)


def receive_message():
    while True:
        try:
            received_msg = connection.recv(BUFFERSIZE).decode("utf8")
            print(received_msg)
        except OSError:  # Possibly client has left the chat.
            break


TCP_IP = "127.0.0.1"
TCP_PORT = 33001
TCP_ADDRESS = (TCP_IP, TCP_PORT)
BUFFERSIZE = 1024

user = launch_login()
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(TCP_ADDRESS)
connection.send(bytes(user, "utf8"))
receive_thread = Thread(target=receive_message)
receive_thread.start()
launch_chatbox(user)
