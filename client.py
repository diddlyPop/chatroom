"""
client.py
Kyle Guss

chatroom client
"""

import PySimpleGUI as sg
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from datetime import datetime
# from sniffrr import Sniffrr

TCP_IP = "167.71.156.224"               # chatroom server IP
LOCAL_IP = "127.0.0.1"                  # loopback IP for testing
TCP_PORT = 33001                        # chatroom server port
TCP_ADDRESS = (TCP_IP, TCP_PORT)        # chatroom server info tuple
AUTH_TOKEN = "1120"                     # current auth token code
BUFFERSIZE = 1024                       # message buffer

sg.change_look_and_feel("DarkAmber")    # PySimpleGUI built-in GUI color change


class Client:

    # loads Client class with initial data. connects to the server with '__setup_flow'.
    # holds our PySimpleGUI layout and window objects
    def __init__(self):
        self.user = None        # NULL username at start
        self.buttons = {"dog": "\n ^..^          /\n/_/\_____/\n     /\   /\\\n    /  \ /  \\"}
        self.colors = ["black", "red", "green", "darkblue"]     # TODO need more colors
        self.connection = None  # NULL connection at start
        self.__setup_flow()     # connect to chatroom server
        self.layout_main = [
            [sg.Multiline("", background_color="black", key="protocol", autoscroll=True, size=(80, 20))],
            [sg.Text('%s: ' % self.user, size=(15, 1)), sg.InputText('', do_not_clear=False)],
            [sg.Submit('Send'), sg.Quit(), sg.Button("dog", button_color=sg.TRANSPARENT_BUTTON,
                                                     image_filename="sprites/dog.png", image_size=(25, 25), image_subsample=5,
                                                     border_width=0)
                                           ]    # TODO reduced colors - black/white/red mode
        ]
        self.window_main = sg.Window('Chat').Layout(self.layout_main)

    # connects to the chatroom server using 'TCP_ADDRESS' tuple
    # sends off current version along with initial connection message
    # deploys a thread to receive broadcasts from the server
    def __setup_flow(self):
        self.launch_login(False)
        self.connection = socket(AF_INET, SOCK_STREAM)  # init socket
        self.connection.connect(TCP_ADDRESS)
        login = "{}-{}".format(self.user, AUTH_TOKEN)
        self.send_message(login, None)  # send name when connected
        user_confirm = self.recv_message()

        while user_confirm != "ACCEPT":
            print("Name in use: ( {} ) or version ( {} ) out-of-date".format(user_confirm, AUTH_TOKEN))
            self.launch_login(True)
            login = "{}-{}".format(self.user, AUTH_TOKEN)
            self.send_message(login, None)  # send name when connected
            user_confirm = self.recv_message()

        receive_thread = Thread(target=self.receive_messages_thread, daemon=True)     # start thread for receiving messages
        receive_thread.start()

    # launch a login window used to capture chatroom username's and display login-errors
    def launch_login(self, retry):
        login_text = "Please choose a username to chat under."
        if retry:
            login_text = "Username is taken or client is out-of-date."
        layout_login = [
            [sg.Text(login_text)],
            [sg.Text('Username: ', size=(15, 1)), sg.InputText('')],
            [sg.Submit(), sg.Quit()]
        ]
        window_login = sg.Window('Login').Layout(layout_login)
        event, values = window_login.Read()
        if values[0] is None:
            exit()
        self.user = values[0]
        window_login.close()

    # launches main gui and contains event loop
    # displays chatbox with custom user from login, calls send_message on 'Submit' event
    def launch_chatbox(self):
        while True:
            event, values = self.window_main.Read()
            if event in (None, 'Quit'):
                self.send_message("/quit", None)  # sends out QUIT message from our client
                break
            elif event in self.buttons:
                self.send_message(self.buttons[event], None)
            else:
                self.send_message(values[0], None)  # SUBMIT sends out message from our client
        self.window_main.close()

    # method to help with message formatting
    def send_message(self, message_to_send, sniff_data):  # send_message transmits client username and message
        if self.user is None:
            title = "N"
        else:
            title = "U"
        message_to_send = title + "@@@" + message_to_send
        if sniff_data is not None:
            message_to_send = message_to_send + "@@@" + sniff_data

        self.connection.send(bytes(message_to_send, "utf8"))

    # method helps with readability
    def recv_message(self):  # recv a message
        return self.connection.recv(BUFFERSIZE).decode("utf8")

    # deploys new thread to receive broadcasts from server
    def receive_messages_thread(self):
        while True:
            try:
                raw = self.recv_message()
                args = raw.split('@@@')
                received_msg = args[1]
                now = datetime.now()
                time = "[" + now.strftime("%H:%M:%S") + "] "
                try:
                    self.printcolor(received_msg[0], time + received_msg)
                except Exception as e:
                    print(e)
            except OSError:  # client left
                break

    # prints messages according to sender's 'title' color
    # uses first letter of name to choose a color
    def printcolor(self, sender, message):
        back_color = "black"
        try:
            sender = sender.lower()
            color = ord(sender) - 97
            back_color = self.colors[color]
        except:
            back_color = "black"
        txt = self.window_main.FindElement("protocol").Widget
        txt.tag_config(sender, background=back_color, foreground="white")
        txt.insert("end", message + "\n", sender)
        self.window_main.FindElement("protocol").Update("", append=True)

    # deploys thread for sniffing unencrypted local network traffic
    # saves photos from this sniffed data into an assets folder on the host computer
    # message protocol can be altered to retransmit image data/who
# def sniffing():
#     S = Sniffrr(15)
#     while True:
#         t.sleep(15)
#         S.TakeSniff()
#         S.CheckSniff()
#         S.AddSniff()

# sniff_thread = Thread(target=sniffing)
# sniff_thread.start()

# TODO need to figure out how to stop user from being able to alter multiline box object on PySimpleGui docs


if __name__ == "__main__":
    C = Client()
    C.launch_chatbox()


