import argparse
import sys
import socket
import struct


def run_server(ip, port):
    print('Running server')
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serv.bind((ip, port))
    except:
        print('Could not bind socket')
        exit(-1)
    serv.listen(1)
    while 1:
        conn, addr = serv.accept()
        data_length = struct.unpack('N', conn.recv(8))[0]
        recvd_data = ""
        while len(recvd_data) != data_length:
            new_data = conn.recv(data_length)
            for b in struct.unpack('<' + 's' * len(new_data), new_data):
                recvd_data += b.decode('utf8')
        print("Received data: " + recvd_data)
        conn.close()


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
        return 0
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
