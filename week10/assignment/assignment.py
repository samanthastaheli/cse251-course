"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Samantha Staheli

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
from configparser import NoSectionError
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2

def writer(shared_list, sem_high, sem_low, values_to_send):
  """ adds numbers to shared_list 
      send numbers to the reader  
      values sent to the readers in consecutive order starting at value 1
      each writer will use all of the sharedList buffer area (ie., BUFFER_SIZE memory positions)
  """
  index = 0
  for i in range(values_to_send):
    sem_high.acquire()

    shared_list[index] = i

    # release low semaphore because an item 
    # was taken from the high semaphore and added to shared_list
    sem_low.release()
    
    # increase the index
    index = (index + 1) % BUFFER_SIZE
  
  # release low semaphore again and 
  sem_low.release()

  # set end index of shared_list to None
  shared_list[index] = None


def reader(shared_list, sem_high, sem_low, values):
  """ A process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process. """
  read_values = 0 # increase 
  index = 0

  while True:
    sem_low.acquire()

    # base case: when at end of shared_list
    # end index is None
    if shared_list[index] == None:
      values[0] = read_values
      return
    
    # go to next number
    read_values += 1

    # print numbers that are in shared_list
    print(shared_list[index])

    # increase the index
    index = (index + 1) % BUFFER_SIZE

    # number has been read so can release from high semaphore
    sem_high.release()

def main():

  # This is the number of values that the writer will send to the reader
  values_to_send = random.randint(1000, 10000)
  # values_to_send = random.randint(1, 50)

  smm = SharedMemoryManager()
  smm.start()

  # amount recived variable, will be increased in reader()
  values = smm.ShareableList([0] * 1) # only need 1 item
  
  # Create a ShareableList to be used between the processes
  # size of shared list is buffer size
  shared_list = smm.ShareableList(range(BUFFER_SIZE))

  # Create any lock(s) or semaphore(s) that you feel you need
  # since shared mem is immutable, use semaphore to "pop()" from list
  # semaphore number will be index number of items in shared list/buffer size
  sem_high = mp.Semaphore(value=BUFFER_SIZE)
  sem_low = mp.Semaphore(value=0)

  # create reader and writer processes
  process_w = mp.Process(target=writer, args=(shared_list, sem_high, sem_low, values_to_send)) 
  process_r = mp.Process(target=reader, args=(shared_list, sem_high, sem_low, values)) 

  # Start the processes and wait for them to finish
  process_w.start()
  process_r.start()

  process_w.join()
  process_r.join()

  print(f'{values_to_send} values sent')

  # Display the number of numbers/items received by the reader.
  # Can not use "items_to_send", must be a value collected by the reader processes.
  print(f'{values[0]} values received')

  smm.shutdown()


if __name__ == '__main__':
    main()
