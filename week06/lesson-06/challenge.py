import multiprocessing
import statistics
import time

# number of seconds to test against
TOTAL_TIME = 10
DONE = "DONE"


def tick(conn):
    # TODO loop over the total time, sleeping for 1
    # second and then send 'time.perf_counter_ns() / 1E9'
        
    # TODO don't forget to send done and close
    
    pass # TODO delete me

def tock(conn, time_stats):
    index = 0
    while True:
        # TODO receive from the pipe, this will
        # block until something is sent
        
        # TODO check if done has been sent
        
        # TODO store the received time stamp in the
        # time stats and increment the index
        
        pass # TODO delete me


def main():

    # TODO create a mp manager list of size TOTAL_TIME
    # call it time_stats
    time_stats = 0

    # TODO create a parent and child pipe

    # TODO create one process that calls tick to send a message
    
    # TODO create one process that calls tock to receive the message

    # TODO start and join the processes back to the main process
    
    
    # The time_stats list should store the received time stamps 
    # and then it will compute the differences between each one.
    # Then it will compute the mean (average) and standard 
    # deviation of the set of differences.
    diff = []
    for index, val in enumerate(time_stats):
        if(index != 0):
            diff.append(val - time_stats[index - 1])
    
    print(f'differences = {diff}')
    print(f'average = {statistics.mean(diff)}')
    print(f'std dev = {statistics.stdev(diff)}')


if __name__ == '__main__':
    main()
