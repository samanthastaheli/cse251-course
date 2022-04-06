"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

from multiprocessing import shared_memory
from multiprocessing.managers import SharedMemoryManager
import time
import random
import multiprocessing as mp
from tracemalloc import start

from cv2 import HOGDESCRIPTOR_DESCR_FORMAT_COL_BY_COL

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 5

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

# -----------------------------------------------------------------------------
def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

# -----------------------------------------------------------------------------
def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))

# -----------------------------------------------------------------------------
def guest_waiting():
    time.sleep(random.uniform(0, 2))

# -----------------------------------------------------------------------------
def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))

# -----------------------------------------------------------------------------
def cleaner(room_population, lock_cleaner, lock_guest, sem_MAX, cleaned_count, start_time, id):
    """
    do the following for TIME seconds
    cleaner will wait to try to clean the room (cleaner_waiting())
    get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    finish_time = time.time() + TIME
    # print(f'{start_time=}')
    # print(f'{finish_time=}')

    while True:
        if time.time() > finish_time:
            break
        # Check if there are guests in the room
        # print(f'{room_population=}')
        lock_cleaner.acquire()
        # print("Lock acquired")
        room_population[1] += 1

        while room_population[0] > 0:
            cleaner_waiting()
        
        # If no one is in the room, start the cleaning message
        print(STARTING_CLEANING_MESSAGE)

        cleaned_count[0] += 1

        cleaner_cleaning(id)

        print(STOPPING_CLEANING_MESSAGE)
        room_population[0] = 0

        lock_cleaner.release()
        sem_MAX.release()

        cleaner_waiting()


# -----------------------------------------------------------------------------
def guest(room_population, lock_cleaner, lock_guest, party_count, start_time, id):
    """
    do the following for TIME seconds
    guest will wait to try to get access to the room (guest_waiting())
    get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    finish_time = time.time() + TIME
    while True:
        if time.time() > finish_time:
            break
        # Check if there are cleaners in the room
        while room_population[1] == 1:
            guest_waiting()
        lock_guest.acquire()

        # If no one is in the room, start the party message
        if room_population[0] == 0:
            while room_population[1] == 1:
                guest_waiting()
            print(STARTING_PARTY_MESSAGE)

        # Share to the cleaners that the room is occupied
        room_population[0] += 1
        lock_guest.release()

        # Add the guest to the total count
        party_count[0] += 1
        # print(party_count)
        
        # Show which guest is in the room
        guest_partying(id)

        # Indicate that the guest left after their time was up
        room_population[0] -= 1

        if room_population[0] == 0:
            print(STOPPING_PARTY_MESSAGE)

        



# -----------------------------------------------------------------------------
def main():
    # add any variables, data structures, processes you need
    # Lock should keep distance between guests and staff
    lock_cleaner = mp.Lock()
    lock_guest = mp.Lock()
    # lock_no_guests = mp.Lock()

    # Semaphore to only allow 1 cleaner into the room
    sem_MAX = mp.Semaphore(1)

    # Sharable list to tell both groups who is in the room
    smm = SharedMemoryManager()
    smm.start()
    room_population = shared_memory.ShareableList([0] * 2)

    # A list to count which types of people go in and out of the room
    cleaned_count = shared_memory.ShareableList([0] * 1)
    party_count = shared_memory.ShareableList([0] * 1)

    # Start time of the running of the program. 
    start_time = time.time()

    # add any arguments to cleaner() and guest() that you need
    cs = []
    hg = []
    for i in range(CLEANING_STAFF):
        id = i
        cs.append(mp.Process(target=cleaner, args=(room_population, lock_cleaner, lock_guest, sem_MAX, cleaned_count, start_time, id + 1)))
        cs[i].start()
    
    for i in range(HOTEL_GUESTS):
        id = i
        hg.append(mp.Process(target=guest, args=(room_population, lock_cleaner, lock_guest, party_count, start_time, id + 1)))
        hg[i].start()

    
    # time.sleep(5)

    for i in range(CLEANING_STAFF):
        cs[i].join()
    
    for i in range(HOTEL_GUESTS):
        hg[i].join()

    # Results
    print(f'Room was cleaned {cleaned_count[0]} times, there were {party_count[0]} parties')


if __name__ == '__main__':
    main()

