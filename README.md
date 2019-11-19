# chatroom
python chatroom displaying networking and communications knowledge

requires python3, PySimpleGui, scapy+npcap (if using sniffrr module)

- clone this directory
- pip3 install PySimpleGui
- run client.py

![](chat.gif)

currently:
- uses tcp connections to transmit messages
- chat server waits for connections
- clients can connect to server to chat
- login prompt and login server messages
- authentication (or verification of users not being a duplicate)
- version verification
- /who server command lists users
- /help shows all server commands
- may have a sniffy suprise if using sniffrr module

hope to add:
- further sniffrr obfuscation and retransmission of image data
- possible message protocols
- enhance gui
- create super chat user
- add server commands
