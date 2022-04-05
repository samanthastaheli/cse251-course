"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: <your name>

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  
  
- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s) or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

Add any comments for me:



"""
from ast import arg
from gzip import READ
from multiprocessing import shared_memory
import random
import time
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 1
WRITERS = 1


def writer(s_list, sem_MAX, sem_DEF, items):
  index = 0
  for i in range(items):
    # Make sure there are no more than 10 numbers are written and
    #    overlapping information not read yet
    sem_MAX.acquire()

    # Write on the current index the value
    s_list[index] = i

    # Increment to the next index. Modulus will keep it within the BUFFER_SIZE range
    index = (index + 1) % BUFFER_SIZE
    sem_DEF.release()

  # Give one more release so the reader can find the 'None' in the list
  sem_DEF.release()
  s_list[index] = None


def reader(s_list, sem_MAX, sem_DEF, values):
  read_items = 0
  index = 0
  while True:
    # Process will wait until at least one number is put into the list
    sem_DEF.acquire()

    # If we reach the end of the list, break out of the while loop
    if s_list[index] == None:
      values[0] = read_items
      return
    read_items += 1

    # Print the numbers received by the writer
    print(s_list[index])

    # Increment to the next index. Modulus will keep it within the BUFFER_SIZE range
    index = (index + 1) % BUFFER_SIZE
    # Let writer know it can write overwrite a new number in the list
    sem_MAX.release()


def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(10, 100)
    print(items_to_send)

    smm = SharedMemoryManager()
    smm.start()

    # Hold the amount received by the writer function
    values = shared_memory.ShareableList([0] * 1)

    # Create a ShareableList to be used between the processes
    shared = shared_memory.ShareableList([0] * BUFFER_SIZE)

    #  Create any lock(s) or semaphore(s) that you feel you need
    sem_MAX = mp.Semaphore(BUFFER_SIZE)
    sem_DEF = mp.Semaphore(0)

    # create reader and writer processes
    writers = []
    for _ in range(WRITERS):
      w = mp.Process(target=writer, args=(shared, sem_MAX, sem_DEF, items_to_send))
      w.start()
      writers.append(w)
    
    readers = []
    for _ in range(READERS):
      r = mp.Process(target=reader, args=(shared, sem_MAX, sem_DEF, values))
      r.start()
      readers.append(r)
    

    # Start the processes and wait for them to finish
    for w in writers:
      w.join()
    
    for r in readers:
      r.join()


    print(f'{items_to_send} values sent')

    # Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')

    print(f'{values[0]} values received')
    smm.shutdown()


if __name__ == '__main__':
    main()