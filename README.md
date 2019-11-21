# chatroom
python chatroom displaying networking and communications knowledge

slides for this program:
https://docs.google.com/presentation/d/1IEoo6ymZyRkoV2EktOFvCBVUxLNVnQsUsKIv519oBHc/edit?usp=sharing

requires python3, PySimpleGui, scapy+npcap (if using sniffrr module)

- git clone https://www.github.com/diddlypop/chatroom.git
- cd chatroom
- pip install -r requirements.txt
- python3 client.py

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
