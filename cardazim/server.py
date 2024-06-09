import argparse
import sys
import socket
import struct


def run_server(ip, port):
    conn = socket.socket()
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((ip, port))
    serv.listen(1)
    while 1:
        conn, addr = serv.accept()
        data_length = struct.unpack('>', conn.recv(4096))


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
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
