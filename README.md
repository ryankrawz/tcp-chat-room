# tcp-chat-room
A TCP-based chat room consisting of a host server connected to a number of client servers through an IP address, port number, and username.

## Host
The host server can connect to the socket and open the chat by executing the following command line, with the second argument being the IP address and the third argument being the port number.
```bash
$ python3 host.py 127.0.0.1 1234
```
The host console prints all activity by users in the chat. The chat can be closed with the `Ctrl+C` interrupt sequence.

## Client
A client server can connect to the socket and enter the chat by executing the following command line, with the second argument being the IP address, the third argument being the port number, and the fourth argument being the client's username. The IP address and port number provided by the client must match those of the host in order for the handshake to succeed.
```bash
$ python3 client.py 127.0.0.1 1234 johndoe
```
All user commands are conducted through the console and executed by the `Enter` key. To send a message to all members of the chat, simply type text into the console.
```
Who all seen the leprechaun say yeah!
```
To send a private message to another member, begin the message with an `@` symbol followed by the username of the recipient.
```
@janedoe This is a special leprechaun flute passed down from thousands of years ago.
```
To query the chat for a list of all active usernames, type the `*` symbol.
```
*
```
A user leaves the chat with the `Ctrl+C` interrupt sequence.
