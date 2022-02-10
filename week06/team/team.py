"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe

After you can copy a text file word by word exactly
- Change the program to be faster (Still using the processes)

"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp
import multiprocessing
from tracemalloc import start 

# Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

PIPECOUNT = 0

def sender(conn, filename1):
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''
    data = open(filename1, 'r')

    for line in data:
        # conn.send('New Line')
        for word in line.split(' '):
            conn.send(word)
    conn.send('DONE')
    conn.close()
        

def receiver(conn, filename2, pipe_count):
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    index = 0
    while True:
        word = conn.recv()

        with open(filename2, 'a') as f:
            if word == 'DONE':
                break
            elif '\n' in word:
                f.write(word)
            else:
                f.write(word + ' ')
            index += 1
            pipe_count.value = index
    conn.close()


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    # TODO create a pipe 
    parent_conn, child_conn = mp.Pipe()

    # TODO create variable to count items sent over the pipe
    pipe_count = Value('i', 0)

    # TODO create processes 
    sender_process = multiprocessing.Process(target=sender, args=(parent_conn, filename1))
    receiver_process = multiprocessing.Process(target=receiver, args=(child_conn, filename2, pipe_count))

    log.start_timer()
    start_time = log.get_time()

    # TODO start processes 
    sender_process.start()
    receiver_process.start()
    # TODO wait for processes to finish
    sender_process.join()
    receiver_process.join()

    stop_time = log.get_time()

    log.stop_timer(f'Total time to transfer content = {pipe_count.value}: ')
    log.write(f'items / second = {pipe_count.value / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    # copy_file(log, 'bom.txt', 'bom-copy.txt')

