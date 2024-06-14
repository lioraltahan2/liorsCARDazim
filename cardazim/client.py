import argparse
import sys
import socket
import struct
from connection import Connection


def send_data(server_ip, server_port, data):
    print('Sending message...')
    with Connection.connect(server_ip, server_port) as conn:
        little_endian_data = struct.pack(
            '<' + 's' * len(data), *[b.encode('utf8') for b in data])
        conn.send_message(little_endian_data)


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('data', type=str,
                        help='the data')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.data)
        print('Done.')
        return 0
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
