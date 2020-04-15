from enum import Enum


class ChatRoomSettings(Enum):
    ARGS_EXCEPTION = 'script requires arguments for IP address, port number, and username'
    ENCODING = 'utf-8'
    MAX_CONNECTIONS = 100
    MESSAGE_LENGTH = 2048
