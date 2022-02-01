"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

"""

from concurrent.futures import thread
import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

RETRIEVE_THREADS = 1        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(q, log, sem_full: threading.Thread):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        check = q.get()
        if (check == NO_MORE_VALUES):
            return

        # TODO process the value retrieved from the queue
        response = requests.get(check)
        data = response.json()

        # TODO make Internet call to get characters name and log it
        log.write(f"{data['name']}")
        sem_full.release()



def file_reader(q, log, sem_full: threading.Thread): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "data.txt" and place items into a queue
    with open('data.txt') as f:
        for line in f:
            if (sem_full._value == 0):
                print('\n########## waiting to acquire sem_empty')
            
            sem_full.acquire()

            q.put(line)

    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"
    for i in range(RETRIEVE_THREADS):
        q.put(NO_MORE_VALUES)


def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    q = queue.Queue()

    # TODO create semaphore (if needed)
    sem_full = threading.Semaphore(20)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    t_fr = threading.Thread(target=file_reader, args=(q, log, sem_full)) 
    t_rt = [threading.Thread(target=retrieve_thread, args=(q, log, sem_full)) for _ in range(RETRIEVE_THREADS)]

    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader
    for t in t_rt:
        t.start()

    t_fr.start()
    # TODO Wait for them to finish - The order doesn't matter
    for t in t_rt:
        t.join()

    t_fr.join()
    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()




