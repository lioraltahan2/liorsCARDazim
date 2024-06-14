import struct
import socket


class ConnectionClosed(Exception):
    "Raised when the connection is closed before all the message is recieved"
    pass


class Connection:

    def __init__(self, connection: socket):
        self.conn = connection

    def __repr__(self):
        return self.conn.__repr__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def send_message(self, message: bytes):
        '''
            Send the message in the connection's socket
        '''
        len_data = struct.pack('N', len(message))
        self.conn.send(len_data)
        self.conn.send(message)

    def recieve_message(self):
        '''
            Recieve message from the connection's socket
        '''
        data_length = struct.unpack('N', self.conn.recv(8))[0]
        recvd_data = bytearray([])
        while len(recvd_data) != data_length:
            try:
                new_data = self.conn.recv(data_length)
            except:
                raise ConnectionClosed
            for b in new_data:
                recvd_data.append(b)
        return bytes(recvd_data)

    @classmethod
    def connect(cls, host, port):
        '''
            Return a connection with socket connected to the given host & port
        '''
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))
        obj = cls(conn)
        return obj

    def close(self):
        '''
            Closes the connection
        '''
        self.conn.close()
