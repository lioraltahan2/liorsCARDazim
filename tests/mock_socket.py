import struct

NUM = 3


class MockSocket:
    sent_data = None
    addr = None

    def __init__(self, can_ignore1, can_ignore2):
        pass

    def connect(self, new_addr):
        self.__class__.addr = new_addr

    def send(self, new_data: bytes):
        self.__class__.sent_data = new_data

    def recv(self, num: int):
        return struct.pack('I', NUM)

    def close(self):
        pass
