import json
import select
import socket
import sys

from utilities import ChatRoomSettings


# AF_INET: address domain of socket
# SOCK_STREAM: type of socket, data read in continuous stream
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) < 4:
    raise Exception(ChatRoomSettings.ARGS_EXCEPTION.value)

# Credentials to initiate handshake
ip_address = sys.argv[1]
port_num = int(sys.argv[2])
username = sys.argv[3]
server.connect((ip_address, port_num))


# Serializes dictionary in JSON format for message to host server
# User input '*' signals a query of all active users
# User input beginning with '@' signals a private message to the username following the '@' symbol
def get_chat_data_json(client_message):
    chat_data = {
        'is_query': False,
        'private_user': '',
        'message': '',
    }
    if client_message == '*':
        chat_data['is_query'] = True
    elif client_message[0] == '@':
        private_user_handle, private_message = client_message.split(' ', 1)
        chat_data['private_user'] = private_user_handle[1:]
        chat_data['message'] = '<{} (private)> {}'.format(username, private_message)
        print('<You:{}> {}'.format(private_user_handle[1:], private_message))
    else:
        chat_data['message'] = '<{}> {}'.format(username, client_message)
        print('<You> {}'.format(client_message))
    return json.dumps(chat_data)


# Send username to host as identifier
while True:
    try:
        server.send(username.encode(ChatRoomSettings.ENCODING.value))
        break
    except OSError:
        continue

# Listen for message from server or input from console
while True:
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        # Message from server
        if socks == server:
            message = socks.recv(ChatRoomSettings.MESSAGE_LENGTH.value)
            if message:
                print(message.decode(ChatRoomSettings.ENCODING.value))
            else:
                print('Sorry, this chat is no longer open\n')
                server.close()
                sys.exit()
        # Input from console
        else:
            message = sys.stdin.readline().strip()
            try:
                json_to_send = get_chat_data_json(message)
                server.send(json_to_send.encode(ChatRoomSettings.ENCODING.value))
            except OSError:
                continue
