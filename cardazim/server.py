from card_manager import CardManager
import argparse
import sys
import threading
from connection import Connection
from listener import Listener
from cards import Card
import struct


def handle_connection(conn, path):
    '''
        Gets a connection to a Client
        Take message from the client and prints it
    '''
    new_data = conn.recieve_message()
    conn.close()
    recvd_card = Card.deserialize(new_data)
    print("Received Card")
    manager = CardManager()
    manager.save(recvd_card, path)
    print("Saved card to path " + path)


def run_server(ip, port, path):
    '''
        Creates a socket in the given ip and port,
        Whenever a connection is accepted, adding a thread handeling that connection
    '''
    print('Running server')
    with Listener(ip, port) as listener:
        while 1:
            connection = listener.accept()
            t1 = threading.Thread(target=handle_connection,
                                  args=(connection, path, ))
            t1.start()


def get_args():
    parser = argparse.ArgumentParser(
        description='Server listening on given ip and port.')
    parser.add_argument('ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('port', type=int,
                        help='the server\'s port')
    parser.add_argument('path', type=str,
                        help='the path where the cards will be saved')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and getting data from clients.
    '''
    args = get_args()
    try:
        run_server(args.ip, args.port, args.path)
        return 0
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
