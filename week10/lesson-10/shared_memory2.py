from multiprocessing import shared_memory
import multiprocessing as mp


def do_work(shared, value, start, end):
    for i in range(start, end):
        shared[i] = value


def main():
    # Create a shared memory block of 100 items
    shared = shared_memory.ShareableList(range(100))

    # Divide the work among two processes, storing partial results in "shared"
    p1 = mp.Process(target=do_work, args=(shared, 1, 0, 50))
    p2 = mp.Process(target=do_work, args=(shared, 2, 50, 100))
    
    

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # we must loop through the shared.buf array to display the values
    print('Buffer values:')
    for i in range(100):
        print(shared[i], end=' ')
    print()


if __name__ == '__main__':
    main()
