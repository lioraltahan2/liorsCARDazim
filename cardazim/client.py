import argparse
import sys
import socket
import struct


def send_data(server_ip, server_port, data):
    print('Sending message...')
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((server_ip, server_port))
    len_data = struct.pack('N', len(data))
    conn.send(len_data)
    little_endian_data = struct.pack(
        '<' + 's' * len(data), *[b.encode('utf8') for b in data])
    conn.send(little_endian_data)
    conn.close()


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
