"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""
​
from multiprocessing import shared_memory
from multiprocessing.managers import SharedMemoryManager
import time
import random
import multiprocessing as mp
from tracemalloc import start
​
from cv2 import HOGDESCRIPTOR_DESCR_FORMAT_COL_BY_COL
​
# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5
​
# Run program for this number of seconds
TIME = 60
​
STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'
​
STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
​
# -----------------------------------------------------------------------------
def cleaner_waiting():
    time.sleep(random.uniform(0, 2))
​
# -----------------------------------------------------------------------------
def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))
​
# -----------------------------------------------------------------------------
def guest_waiting():
    time.sleep(random.uniform(0, 2))
​
# -----------------------------------------------------------------------------
def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))
​
# -----------------------------------------------------------------------------
def cleaner(room_population, room_key, sem_MAX, cleaned_count, start_time, id):
    """ When there are no people in the room, have a chance to clean the room """
    # Create a final time for the program to exit
    finish_time = start_time + TIME
    while True:
        # Break out of loop when we reach the final time
        if time.time() > finish_time:
            break
        
        # Only one cleaner per room
        sem_MAX.acquire()
​
        # Collect the room key to enter the room if avaliable
        room_key.acquire()
​
        # Turn on the lights if someone is the first to enter the room
        if room_population[1] == 0:
            print(STARTING_CLEANING_MESSAGE)
            # Add one so future cleaners don't repeat turning on lights while they are already on
            room_population[1] += 1
        
        # Add the cleaner to the total count
        cleaned_count[0] += 1
​
        # Cleaners clean hard for about 2 seconds
        cleaner_cleaning(id)
​
        # Indicate that the cleaner left after their time was up
        room_population[1] -= 1
        
        # Turn off the lights if someone is the last to leave the room
        print(STOPPING_CLEANING_MESSAGE)
        # Give the key back to the lobby
        room_key.release()
        cleaner_waiting()
        sem_MAX.release()
​
​
​
# -----------------------------------------------------------------------------
def guest(room_population, room_key, organizing_lock, party_count, start_time, id):
    """ When there are no people in the room, have a chance to start a party """
    # Create a final time for the program to exit
    finish_time = start_time + TIME
    while True:
        # Break out of loop when we reach the final time
        if time.time() > finish_time:
            break
        
        # If there are cleaners in the room, wait for them to finish
        while room_population[1] > 0:
            guest_waiting()
​
        # A lock to allow only one person to enter at a time
        organizing_lock.acquire()
        # Increase the room size by one
        room_population[0] += 1
        # Turn on the lights if someone is the first to enter the room
        if room_population[0] == 1:
            # Collect the room key to enter the room if avaliable
            room_key.acquire()
            # Add an instance of how many parties were started
            party_count[0] += 1
            print(STARTING_PARTY_MESSAGE)
​
        # Let the next person enter the party
        organizing_lock.release()
​
        # Guest partys hard for about 1 second
        guest_partying(id)
​
        # Turn off the lights if someone is the last to leave the room
        # Let people leave the room in an ordered fashion
        organizing_lock.acquire()
        room_population[0] -= 1
        # If there is one last person leaving the party...
        if room_population[0] == 0:
            # ...Turn off the lights and return the key
            print(STOPPING_PARTY_MESSAGE)
            # Give the key back to the lobby
            room_key.release()
​
        # Release the person leaving the room
        organizing_lock.release()
        # Have the guest do something for a few seconds outside of the room
        guest_waiting()
​
​
​
​
# -----------------------------------------------------------------------------
def main():
    # add any variables, data structures, processes you need
    # Lock should keep distance between guests and staff
    room_key = mp.Lock()
    organizing_lock = mp.Lock()
​
    # Semaphore to only allow 1 cleaner into the room
    sem_MAX = mp.Semaphore(1)
​
    # Sharable list to tell both groups who is in the room
    smm = SharedMemoryManager()
    smm.start()
    room_population = smm.ShareableList([0] * 2)
​
    # A list to count which types of people go in and out of the room
    cleaned_count = smm.ShareableList([0] * 1)
    party_count = smm.ShareableList([0] * 1)
​
    # Start time of the running of the program. 
    start_time = time.time()
​
    # add any arguments to cleaner() and guest() that you need
    cs = []
    hg = []
    for i in range(CLEANING_STAFF):
        id = i
        cs.append(mp.Process(target=cleaner, args=(room_population, room_key, sem_MAX, cleaned_count, start_time, id + 1)))
        cs[i].start()
    
    for i in range(HOTEL_GUESTS):
        id = i
        hg.append(mp.Process(target=guest, args=(room_population, room_key, organizing_lock, party_count, start_time, id + 1)))
        hg[i].start()
​
    
    # time.sleep(5)
​
    for i in range(CLEANING_STAFF):
        cs[i].join()
    
    for i in range(HOTEL_GUESTS):
        hg[i].join()
​
    # Results
    print(f'Room was cleaned {cleaned_count[0]} times, there were {party_count[0]} parties')
​
​
if __name__ == '__main__':
    main()