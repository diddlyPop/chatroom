import PySimpleGUI as simpleg

def launch_login():
    layout = [
        [simpleg.Text('Please choose a username to chat under.')],
        [simpleg.Text('Username: ', size=(15, 1)), simpleg.InputText('')],
        [simpleg.Submit(), simpleg.Cancel()]
    ]
    window = simpleg.Window('Login').Layout(layout)
    button, values = window.Read()
    user = values[0]
    window.close()
    return user

def launch_chatbox(user):
    layout = [
        [simpleg.Text('%s: ' % user, size=(15, 1)), simpleg.InputText('')],
        [simpleg.Submit('Send'), simpleg.Cancel()]
    ]
    window = simpleg.Window('Chat').Layout(layout)
    button, values = window.Read()


if __name__ == '__main__':
    user = launch_login()
    launch_chatbox(user)