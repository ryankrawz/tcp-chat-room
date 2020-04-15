import json
import socket
import sys
from threading import enumerate, Thread

from utilities import ChatRoomSettings


# AF_INET: address domain of socket
# SOCK_STREAM: type of socket, data read in continuous stream
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) < 3:
    raise Exception(ChatRoomSettings.ARGS_EXCEPTION.value)

ip_address = sys.argv[1]
port_num = int(sys.argv[2])
# Bind server to provided IP address and port number, client must have same information to initiate handshake
server.bind((ip_address, port_num))
# Listens for a specified number of server connections
server.listen(ChatRoomSettings.MAX_CONNECTIONS.value)
# Dictionary of all active clients in chat room mapping username to client server connection
active_clients = dict()


# Initializes parallel process for receiving data from and sending data to specific client server
def client_thread(name):
    connection = active_clients[name]
    connection.send('Welcome to the chat!'.encode(ChatRoomSettings.ENCODING.value))
    while True:
        try:
            chat_data = get_chat_data(name)
            if chat_data:
                # Client is querying active user list
                if chat_data['is_query']:
                    query_string = get_active_user_string(name)
                    connection.send(query_string.encode(ChatRoomSettings.ENCODING.value))
                    print('{} queried active users'.format(name))
                # Client is sending private message
                elif chat_data['private_user']:
                    private_connection = active_clients.get(chat_data['private_user'], None)
                    if private_connection:
                        private_connection.send(chat_data['message'].encode(ChatRoomSettings.ENCODING.value))
                        print('<{} to {}> {}'.format(name, chat_data['private_user'], chat_data['message']))
                    else:
                        no_user_message = '{} isn\'t currently active in the chat'.format(chat_data['private_user'])
                        connection.send(no_user_message.encode(ChatRoomSettings.ENCODING.value))
                        print('The message from {} to {} failed since {}'.format(
                            name,
                            chat_data['private_user'],
                            no_user_message,
                        ))
                # Client is sending message to all active users
                else:
                    broadcast(chat_data['message'].encode(ChatRoomSettings.ENCODING.value), name)
                    print(chat_data['message'])
        except InterruptedError:
            continue


# Transmits message to all client server connections
def broadcast(message, name):
    for client_username in active_clients:
        if client_username != name:
            try:
                active_clients[client_username].send(message)
            except InterruptedError:
                active_clients[client_username].close()
                remove(client_username)


# Serializes list of all active users based on username
def get_active_user_string(name):
    query_string = 'All active users:'
    for client_username in active_clients:
        self_identifier = ' (You)' if client_username == name else ''
        query_string += '\n' + client_username + self_identifier
    return query_string


# Retrieves data in JSON format from client server connection
def get_chat_data(name):
    message = active_clients[name].recv(ChatRoomSettings.MESSAGE_LENGTH.value).decode(ChatRoomSettings.ENCODING.value)
    if message:
        return json.loads(message)
    remove(name)
    return None


# Listens for first message from client server connection signifying username
def get_username_from_client(connection):
    while True:
        try:
            return connection.recv(ChatRoomSettings.MESSAGE_LENGTH.value).decode(ChatRoomSettings.ENCODING.value)
        except InterruptedError:
            continue


# Closes connection of client server and removes it from active users
def remove(name):
    active_clients[name].close()
    del active_clients[name]


try:
    while True:
        # Accept connection request consisting of socket object and client IP address
        user_connection, user_address = server.accept()
        username = get_username_from_client(user_connection)
        active_clients[username] = user_connection
        new_client_thread = Thread(target=client_thread, args=username)
        new_client_thread.start()
        print('{} has now connected'.format(username))
except KeyboardInterrupt:
    for info in active_clients:
        info[0].close()
    for thread in enumerate():
        thread.join()
    server.close()
    print('Chat closed\n')
    sys.exit()
