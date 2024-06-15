import argparse
import sys
import socket
from connection import Connection
from cards import Card
from crypt_image import CryptImage

key = 'super secret key'


def send_data(server_ip, server_port, name, creator, path, riddle, solution):
    card = Card.create_from_path(name, creator, path, riddle, solution)
    print('Sending ' + str(card))
    card.image.encrypt(key)
    with Connection.connect(server_ip, server_port) as conn:
        conn.send_message(card.serialize())


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('name', type=str,
                        help='the cards name')
    parser.add_argument('creator', type=str,
                        help='the cards name')
    parser.add_argument('path', type=str,
                        help='the path to the image')
    parser.add_argument('riddle', type=str,
                        help='the riddle')
    parser.add_argument('solution', type=str,
                        help='the solution for the riddle')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.name,
                  args.creator, args.path, args.riddle, args.solution)
        print('Done.')
        return 0
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
