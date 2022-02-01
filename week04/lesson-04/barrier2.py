# Two processes with multiple stages

import threading
import queue
import multiprocessing as mp
import requests
import time


def process1(process_id, barrier):
    start_time = time.perf_counter()

    # Init
    time.sleep(1)
    barrier.wait()  # Wait for all processes to complete the task before printing
    print(f'{process_id} After init\n')

    # proces data
    time.sleep(2)
    barrier.wait()  # Wait for all processes to complete the task before printing
    print(f'{process_id} After process data\n')

    # clean up of data
    time.sleep(1)
    barrier.wait()  # Wait for all processes to complete the task before printing
    print(f'{process_id} After clean up\n')


def process2(process_id, barrier):
    start_time = time.perf_counter()

    # Init
    time.sleep(2)
    barrier.wait()  # Wait for all processes to complete the task before printing
    print(f'{process_id} After init\n')

    # proces data
    time.sleep(1)
    barrier.wait()  # Wait for all processes to complete the task before printing
    print(f'{process_id} After process data\n')

    # clean up of data
    time.sleep(2)
    barrier.wait()  # Wait for all processes to complete the task before printing
    print(f'{process_id} After clean up\n')

def main():

    barrier = mp.Barrier(4)        

    # Create 4 processes, pass a "process_id" for each thread
    processes = []
    processes.append(mp.Process(target=process1, args=(1, barrier)))
    processes.append(mp.Process(target=process2, args=(2, barrier)))
    processes.append(mp.Process(target=process1, args=(3, barrier)))
    processes.append(mp.Process(target=process2, args=(4, barrier)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()


if __name__ == '__main__':
    main()