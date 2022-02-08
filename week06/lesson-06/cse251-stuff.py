import ctypes
import threading
import multiprocessing
import queue
import time


def f1(n):
    print(n)


def f2(n1, n2, n3):
    print(n1)
    print(n2)
    print(n3)


def s1(sem: threading.Semaphore, lock: threading.Lock, barrier: threading.Barrier, que: queue.Queue):
    for i in range(5):
        # protect the queue
        lock.acquire()

        # add to queue
        que.put(time.time())

        # release lock
        lock.release()

        # this will tell the other thread blocked on acquire to proceed and read the queue
        sem.release()

    # wait for all the threads before proceeding
    barrier.wait()

    # notify queue readers that nothing more is being added
    lock.acquire()
    que.put(None)
    lock.release()
    # tell reading thread to read one more time
    sem.release()


def s2(sem: threading.Semaphore, lock: threading.Lock, que: queue.Queue):
    while True:
        # this will block until release is called on other thread that
        # is adding things to the queue
        sem.acquire()

        # lock and get from queue
        lock.acquire()
        item = que.get()
        lock.release()

        # check if done
        if(item == None):
            return

        print(f'queue message = {item}')


def send(conn: multiprocessing.Pipe):
    for i in range(5):
        # Send the message through the pipe connection
        conn.send(time.time())
        time.sleep(0.5)

    # done
    conn.send(None)

    # close connection
    conn.close()


def receive(conn: multiprocessing.Pipe):
    while True:
        # Get the message through the pipe connection
        msg = conn.recv()
        if(msg == None):
            break
        print(f'pipe message = {msg}')

    # close connection
    conn.close()


def main():

    ###############################
    # THREADING
    ###############################

    regular_list = [1, 2, 3]

    # Semaphores
    sem = threading.Semaphore(0)

    # Locks
    lock = threading.Lock()

    # Barriers
    barrier = threading.Barrier(1)

    # Queues
    que = queue.Queue()

    # Threads
    t1 = threading.Thread(target=s1, args=(sem, lock, barrier, que))

    t2 = threading.Thread(target=s2, args=(sem, lock, que))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    ###############################
    # MULTIPROCESSING
    ###############################

    # Manager Lists
    mp_list = multiprocessing.Manager().list(regular_list)

    # Processes
    p1 = multiprocessing.Process(target=f1, args=(mp_list,))
    p1.start()
    p1.join()

    p2 = multiprocessing.Process(target=f1, args=(mp_list,))
    p2.start()
    print(p2.is_alive())
    p2.terminate()

    # Pools and maps
    with multiprocessing.Pool(3) as p:
        # this will create 3 processes and divide up the elements fairly among them.
        # Then it will pass each element to the 'f1 function
        p.map(f1, mp_list)

        list_of_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        with multiprocessing.Pool(3) as p:
            # this will divide the list into 3 fair (equal-ish) sized lists
            # and pass the sublist to the 'f' function. Need to use 'starmap'
            # to divide up the sublist into 3 elements to be passed to 'f2'
            p.starmap(f2, list_of_lists)

    # Values - mp variable
    num = multiprocessing.Value(ctypes.c_double, 10.0)

    # Arrays - mp varable
    arr = multiprocessing.Array(ctypes.c_int, range(10))

    # Pipes
    parent, child = multiprocessing.Pipe()
    p3 = multiprocessing.Process(target=send, args=(parent,))
    p4 = multiprocessing.Process(target=receive, args=(child,))

    p3.start()
    p4.start()
    p3.join()
    p4.join()


if __name__ == '__main__':
    main()
