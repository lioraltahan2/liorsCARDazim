import socket
from connection import Connection


class Listener:

    def __init__(self, host, port, backlog=1000):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

    def __repr__(self):
        return "Listener(port = {}, host = {}, backlog = {}".format(self.port, self.host, self.backlog)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stop()

    def start(self):
        '''
            Start listenning
        '''
        self.sock.listen(self.backlog)

    def stop(self):
        '''
            Stop listenning and close the sockets
        '''
        self.sock.close()

    def accept(self):
        '''
            Accept a connection, returns the connection as Connection object
        '''
        conn, addr = self.sock.accept()
        return Connection(conn)
