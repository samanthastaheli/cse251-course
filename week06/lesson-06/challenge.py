import multiprocessing
import statistics
import time

# number of seconds to test against
TOTAL_TIME = 10
DONE = "DONE"


def tick(conn):
    # DONE loop over the total time, sleeping for 1
    # second and then send 'time.perf_counter_ns() / 1E9'
    for _ in range(TOTAL_TIME):
        time.sleep(1)
        conn.send(time.perf_counter_ns() / 1E9)

    # DONE don't forget to send done and close
    conn.send(DONE)
    conn.close()

def tock(conn, time_stats):
    index = 0
    while True:
        # DONE receive from the pipe, this will
        # block until something is sent
        msg = conn.recv()

        # DONE check if done has been sent
        if msg == DONE:
            break

        # DONE store the received time stamp in the
        # time stats and increment the index
        time_stats[index] = msg
        index += 1


def main():

    # DONE create a mp manager list of size TOTAL_TIME
    # call it time_stats
    time_stats = multiprocessing.Manager().list([0] * TOTAL_TIME) # creates list that can be shared between processes

    # TODO create a parent and child pipe
    parent_conn, child_conn = multiprocessing.Pipe()

    # TODO create one process that calls tick to send a message
    tick_process = multiprocessing.Process(target=tick, args=(parent_conn,))

    # TODO create one process that calls tock to receive the message
    tock_process = multiprocessing.Process(target=tock, args=(child_conn, time_stats))

    # TODO start and join the processes back to the main process
    tick_process.start()
    tock_process.start()
    tick_process.join()
    tock_process.join()

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
