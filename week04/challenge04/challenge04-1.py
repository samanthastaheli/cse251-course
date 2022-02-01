import threading
import queue
import time
import random

# Include cse 251 common Python files
RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

max_size = 0

def processor(q, sem_empty: threading.Semaphore, sem_full: threading.Semaphore):
    
    # Use this to print out the max_size of your queue to ensure
    # that you never had more than 20 items in your queue
    global max_size

    while True:
        
        # TODO semaphore acquire/release?

        pair = q.get()  # touple of (number, power)
        if (pair == NO_MORE_VALUES):
            return
        
        # Store off the max size
        if (q.qsize() > max_size):
            max_size = q.qsize()

        # Get the number and power
        number, power = pair
        
        # print out answer (with number of power shown)
        print(f'{number}^{power} = {number ** power}')
        
        # leave this
        time.sleep(random.uniform(0.001, 0.009))
        
        # TODO semaphore acquire/release?

def reader(q, sem_empty: threading.Semaphore, sem_full: threading.Semaphore):

    # TODO read in a line from numbers.txt and put it in the queue.
    # Ensure that the maximum queue size is never more than 20 by
    # using the sem_empty semaphore 
    with open('numbers.txt') as f:
        for line in f:
            
            # leave this
            if(sem_empty._value == 0):
                print('\n########## waiting to acquire sem_empty')
                
            # TODO semaphore acquire/release?
            
            # the line will be like 1234,3
            # split(',') will split the string on the comma and
            # return a list of two numbers
            
            # put the numbers on the queue as a touple---wrap the numbers in ()
            
            # TODO semaphore acquire/release?
            
            # leave this
            time.sleep(random.uniform(0.001, 0.01))
        
    print('\n\nFinished reading the file\n\n')
    
    # Signal to processor that there are no more value

def main():
    begin_time = time.perf_counter()
    
    # TODO create a queue
    
    # TODO create a semaphore with a counter starting at 20
    
    # TODO create a semaphore with a default counter

    # TODO create one reader thread
    
    # TODO create one processor thread
 
    # TODO start your processor threads first
    
    # TODO then start your reader thread

    # TODO join reader thread
    
    # TODO join processer thread

    print(f'Time to process all numbers: {time.perf_counter() - begin_time} sec')
    print(f'{max_size = }')

if __name__ == '__main__':
    main()