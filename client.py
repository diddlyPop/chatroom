"""
client.py
Kyle Guss

chatroom client
"""

import PySimpleGUI as simpleg
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
#from sniffrr import Sniffrr


def launch_login(retry):     # displays login prompt and returns user login
    login_text = "Please choose a username to chat under."
    if retry:
        login_text = "Username is taken. Choose a new name."
    layout = [
        [simpleg.Text(login_text)],
        [simpleg.Text('Username: ', size=(15, 1)), simpleg.InputText('')],
        [simpleg.Submit(), simpleg.Quit()]
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
        [simpleg.Submit('Send'), simpleg.Quit()]
    ]
    window = simpleg.Window('Chat').Layout(layout)
    while True:
        event, values = window.Read()
        if event in (None, 'Quit'):
            send_message("[quit]")  # sends out QUIT message from our client
            break
        else:
            send_message(values[0])   # SUBMIT sends out message from our client
    window.close()


def send_message(message_to_send):    # send_message transmits client username and message
    connection.send(bytes(message_to_send, "utf8"))


def receive_message():
    while True:
        try:
            received_msg = connection.recv(BUFFERSIZE).decode("utf8")
            print(received_msg)
        except OSError:  # client left
            break


# def sniffing():
#     S = Sniffrr(15)
#     while True:
#         t.sleep(15)
#         S.TakeSniff()
#         S.CheckSniff()
#         S.AddSniff()



# socket info
TCP_IP = "167.71.156.224"
TCP_PORT = 33001
TCP_ADDRESS = (TCP_IP, TCP_PORT)
BUFFERSIZE = 1024

user = launch_login(False)   # get user from login window

connection = socket(AF_INET, SOCK_STREAM)  # init socket
connection.connect(TCP_ADDRESS)
connection.send(bytes(user, "utf8"))    # send name when connected

user_confirm = connection.recv(BUFFERSIZE).decode("utf8")
while user_confirm == "DENY":
    print("Name in use: ( {} ) ".format(user_confirm))
    user = launch_login(True)
    connection.send(bytes(user, "utf8"))  # send name when connected
    user_confirm = connection.recv(BUFFERSIZE).decode("utf8")


receive_thread = Thread(target=receive_message, daemon=True)     # start thread for receiving messages
receive_thread.start()

#sniff_thread = Thread(target=sniffing)          # requires Scapy
#sniff_thread.start()

launch_chatbox(user)    # start chatbox gui under client username


