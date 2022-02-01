import multiprocessing
import time
import datetime


def test_with_barrier(name, synchronizer: multiprocessing.Barrier, serializer):
    synchronizer.wait()
    now = time.time()
    
    # I'm using serializer here to ensure the two 
    # processes print correctly (without printing on the same line)
    with serializer:
        print(f'process {name} - {now}')


def test_without_barrier(name):
    now = time.time()
    print(f'process {name} - {now}')


if __name__ == '__main__':
    synchronizer = multiprocessing.Barrier(2)
    serializer = multiprocessing.Lock()

    multiprocessing.Process(target=test_with_barrier, args=(
        'p1 - test_with_barrier', synchronizer, serializer)).start()
    
    multiprocessing.Process(target=test_with_barrier, args=(
        'p2 - test_with_barrier', synchronizer, serializer)).start()
    
    multiprocessing.Process(target=test_without_barrier, args=(
        'p3 - test_without_barrier', )).start()
    
    multiprocessing.Process(target=test_without_barrier, args=(
        'p4 - test_without_barrier', )).start()
