import argparse
import sys
import socket
import struct
import threading
from connection import Connection
from listener import Listener
import time

lock = threading.Lock()


def handle_connection(conn):
    '''
        Gets a connection to a Client
        Take message from the client and prints it
    '''
    time.sleep(10)
    new_data = conn.recieve_message()
    recvd_data = ""
    for b in struct.unpack('<' + 's' * len(new_data), new_data):
        recvd_data += b.decode('utf8')
    print("Received data: " + recvd_data)
    conn.close()


def run_server(ip, port):
    '''
        Creates a socket in the given ip and port,
        Whenever a connection is accepted, adding a thread handeling that connection
    '''
    print('Running server')
    with Listener(ip, port) as listener:
        while 1:
            connection = listener.accept()
            t1 = threading.Thread(target=handle_connection,
                                  args=(connection,))
            t1.start()


def get_args():
    parser = argparse.ArgumentParser(
        description='Server listening on given ip and port.')
    parser.add_argument('ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and getting data from clients.
    '''
    args = get_args()
    try:
        run_server(args.ip, args.port)
        return 0
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
