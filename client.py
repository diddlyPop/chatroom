"""
client.py
Kyle Guss

chatroom client
"""

import PySimpleGUI as sg
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from datetime import datetime
import random
# from sniffrr import Sniffrr


def launch_login(retry):     # displays login prompt and returns user login
    login_text = "Please choose a username to chat under."
    if retry:
        login_text = "Username is taken or client is out-of-date."
    layout = [
        [sg.Text(login_text)],
        [sg.Text('Username: ', size=(15, 1)), sg.InputText('')],
        [sg.Submit(), sg.Quit()]
    ]
    window = sg.Window('Login').Layout(layout)
    event, values = window.Read()
    user = values[0]
    window.close()
    return user


def launch_chatbox(user):   # displays chatbox with custom user from login, calls send_message
    while True:
        event, values = window_main.Read()
        if event in (None, 'Quit'):
            send_message("/quit")  # sends out QUIT message from our client
            break
        elif event == "dog":
            send_message("\n ^..^          /\n/_/\_____/\n     /\   /\\\n    /  \ /  \\")
        else:
            send_message(values[0])   # SUBMIT sends out message from our client
    window_main.close()


def send_message(message_to_send):    # send_message transmits client username and message
    connection.send(bytes(message_to_send, "utf8"))


def receive_message():
    while True:
        now = datetime.now()
        time = "[" + now.strftime("%H:%M:%S") + "] "
        try:
            received_msg = connection.recv(BUFFERSIZE).decode("utf8")
            printcolor(received_msg[0], time + received_msg)
        except OSError:  # client left
            break


def printcolor(sender, message):
    back_color = "black"
    try:
        sender = sender.lower()
        color = ord(sender) - 97
        back_color = colors[color]
    except:
        back_color = "black"
    txt = window_main.FindElement("protocol").Widget
    txt.tag_config(sender, background=back_color, foreground="white")
    txt.insert("end", message + "\n", sender)
    window_main.FindElement("protocol").Update("", append=True)


# def sniffing():
#     S = Sniffrr(15)
#     while True:
#         t.sleep(15)
#         S.TakeSniff()
#         S.CheckSniff()
#         S.AddSniff()


# socket info
TCP_IP = "167.71.156.224"
LOCAL_IP = "127.0.0.1"
TCP_PORT = 33001
TCP_ADDRESS = (TCP_IP, TCP_PORT)
AUTH_TOKEN = "1111"
BUFFERSIZE = 1024

colors = ["black", "red", "darkyellow", "darkblue"]

user = launch_login(False)   # get user from login window

connection = socket(AF_INET, SOCK_STREAM)  # init socket
connection.connect(TCP_ADDRESS)

login = "{}-{}".format(user, AUTH_TOKEN)

connection.send(bytes(login, "utf8"))    # send name when connected

user_confirm = connection.recv(BUFFERSIZE).decode("utf8")

while user_confirm != "ACCEPT":
    print("Name in use: ( {} ) or version ( {} ) out-of-date".format(user_confirm, AUTH_TOKEN))
    user = launch_login(True)
    login = "{}-{}".format(user, AUTH_TOKEN)
    connection.send(bytes(login, "utf8"))  # send name when connected
    user_confirm = connection.recv(BUFFERSIZE).decode("utf8")

receive_thread = Thread(target=receive_message, daemon=True)     # start thread for receiving messages
receive_thread.start()

# sniff_thread = Thread(target=sniffing)          # requires Scapy
# sniff_thread.start()

# TODO need to figure out how to stop user from being able to alter multiline box object on PySimpleGui docs
layout_main = [
    [sg.Multiline("", key="protocol", autoscroll=True, size=(80, 20))],
    [sg.Text('%s: ' % user, size=(15, 1)), sg.InputText('', do_not_clear=False)],
    [sg.Submit('Send'), sg.Quit(), sg.Button("dog", button_color=sg.TRANSPARENT_BUTTON,
                                             image_filename="dog.png", image_size=(50, 50), image_subsample=2,
                                             border_width=0)]
]
window_main = sg.Window('Chat').Layout(layout_main)

launch_chatbox(user)    # start chatbox gui under client username


