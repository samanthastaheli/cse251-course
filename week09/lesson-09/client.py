import socket
import pickle
import time
from ProcessData import ProcessData
from threading import Thread
import random
import string


HOST = 'localhost'
PORT = 11007

users = ["Aaron", "Brandon", "Carey", "David",
         "Eugene", "Frank", "George", "Henry"]


class producer(Thread):
    pass


def main():

    # TODO create socket connection (use AF_INET for IPv4 and socket stream-->TCP protocol)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT)) # (HOST, PORT) is tuple
    
    # create some data to send over
    user_ids = [i for i in range(1, 101)]

    datas = []
    for i in range(10):
        data = ProcessData()
        data.task_id = i
        data.start_time = time.process_time_ns()
        data.user_name = random.choice(users)
        data.user_id = user_ids.pop()
        datas.append(data)

    # TODO create some threads to send data to server
    threads = []
    for i in range(10): # 1 for each data you created
        threads.append(producer(s, data[i]))
    
    for t in threads:
        t.start()
        
    for t in threads:
        t.join()

    print()
    # TODO create one last data with close_connection set to true

    # TODO close socket connection
    

if __name__ == '__main__':
    main()
    print('All data sent and client side of socket is closed')
