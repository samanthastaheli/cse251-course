import multiprocessing as mp
import time
import os

def square(value):
    value **= 2 # square then assign back to value
    print(f'called function in process: , pid={os.getpid()}')
    time.sleep(0.01)
    return value
    

if __name__ == '__main__':
    inputs = list(range(101)) #0 to 100
    
    # 1st way
    pool = mp.Pool(processes=4)
    outputs = pool.map(square, inputs)
    pool.close()
    pool.join()
    print(f'\n1st Way Pool: {outputs}')
    
    # OR
    
    # 2nd way
    with mp.Pool(processes=4) as p:
        outputs = p.map(square, inputs)
    print(f'\n2nd Way Pool: {outputs}')