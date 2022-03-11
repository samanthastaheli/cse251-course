from multiprocessing import shared_memory
import multiprocessing as mp


def do_work(shared_name, value, start, end):
    # attach to an existing shared mem
    shared = shared_memory.SharedMemory(shared_name)
    for i in range(start, end):
        shared.buf[i] = value
    # need to close this local shared mem block access
    shared.close()

def main():
    shared = shared_memory.SharedMemory(create=True, size=100)
    # create shared mem block 100 times
    print(f'Shared memory name = {shared.name}')

    # divide work amount 2 processess
    # store partial resilts in shared
    p1 = mp.Process(target=do_work, args=(shared.name, 1, 0, 50))
    p2 = mp.Process(target=do_work, args=(shared.name, 2, 50, 100))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print('Buffer values:')
    for i in range(100):
        print(shared.buf[i], end=', ')

    print()

    # close and give memory block back to the OS
    shared.close()
    shared.unlink()

if __name__ == '__main__':
    main()