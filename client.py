import PySimpleGUI as simpleg

layout = [
          [simpleg.Text('Please enter your Name, Address, Phone')],
          [simpleg.Text('Name', size=(15, 1)), simpleg.InputText('name')],
          [simpleg.Text('Address', size=(15, 1)), simpleg.InputText('address')],
          [simpleg.Text('Phone', size=(15, 1)), simpleg.InputText('phone')],
          [simpleg.Submit(), simpleg.Cancel()]
         ]

window = simpleg.Window('Simple data entry window').Layout(layout)
button, values = window.Read()

print(button, values[0], values[1], values[2])