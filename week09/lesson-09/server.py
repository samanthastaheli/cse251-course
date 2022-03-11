import socket
import pickle
import time
from ProcessData import ProcessData

HOST = 'localhost'
PORT = 11007


def main():
    # TODO create socket, bind, listen and loop to get data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind()



if __name__ == '__main__':
    main()
    print('Server connection closed')
