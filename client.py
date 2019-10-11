import PySimpleGUI as simpleg
import socket
import os

def send_message(message):
    pass

def launch_login():
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

def launch_chatbox(user):
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
            print("{0}: {1}".format(user, values[0]))
            send_message(values[0])
    window.Close()

if __name__ == '__main__':
    user = launch_login()
    launch_chatbox(user)
