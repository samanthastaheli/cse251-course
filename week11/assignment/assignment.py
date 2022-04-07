"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

from multiprocessing.managers import SharedMemoryManager
import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))

def cleaner(cleaner_lock, room_key, start_time, cleaned_count, cleaner_id):
    """
    do the following for TIME seconds
    cleaner will wait to try to clean the room (cleaner_waiting())
    get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    finish_time = start_time + TIME

    while True:
        if time.time() > finish_time:
            return

        cleaner_lock.acquire()
        room_key.acquire()
        cleaned_count[0] += 1
        print(STARTING_CLEANING_MESSAGE)
        cleaner_cleaning(cleaner_id)

        print(STOPPING_CLEANING_MESSAGE)

        room_key.release()
        cleaner_lock.release()
        
        cleaner_waiting()

def guest(room_key, start_time, party_count, guest_id, room_pop, organizing_lock):
    """
    do the following for TIME seconds
    guest will wait to try to get access to the room (guest_waiting())
    get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    finish_time = start_time + TIME

    while True:
        if time.time() > finish_time:
            return

        organizing_lock.acquire()

        room_pop[0] += 1

        if room_pop[0] == 1:
            room_key.acquire()
            party_count[0] += 1
            print(STARTING_PARTY_MESSAGE)

        organizing_lock.release()
        guest_partying(guest_id)
        organizing_lock.acquire()
        room_pop[0] -= 1

        if room_pop[0] == 0:
            room_key.release()
            print(STOPPING_PARTY_MESSAGE)
            
        organizing_lock.release()
        guest_waiting()

def main():
    # TODO - add any variables, data structures, processes you need
    # TODO - add any arguments to cleaner() and guest() that you need

    smm = SharedMemoryManager()
    smm.start()
    # smm.join()

    cleaned_count = smm.ShareableList([0] * 1)
    party_count = smm.ShareableList([0] * 1)
    room_pop = smm.ShareableList([0] * 2) # amount of guest and cleaners in room

    # 2 locks required
    cleaner_lock = mp.Lock()
    room_key = mp.Lock()
    organizing_lock = mp.Lock()

    # Start time of the running of the program. 
    start_time = time.time()

    cleaner_list = []
    for i in range(CLEANING_STAFF):
        cleaner_id = i + 1
        cleaner_list.append(mp.Process(target=cleaner, args=(cleaner_lock, room_key, start_time, cleaned_count, cleaner_id)))
        cleaner_list[i].start()
    
    guest_list = []
    for i in range(HOTEL_GUESTS):
        guest_id = i + 1
        guest_list.append(mp.Process(target=guest, args=(room_key, start_time, party_count, guest_id, room_pop, organizing_lock)))
        guest_list[i].start()
        
    for i in range(CLEANING_STAFF):
        cleaner_list[i].join()

    for i in range(HOTEL_GUESTS):
        guest_list[i].join()

    # Results
    print(f'Room was cleaned {cleaned_count[0]} times, there were {party_count[0]} parties')


if __name__ == '__main__':
    main()
