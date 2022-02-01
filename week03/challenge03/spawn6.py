import multiprocessing as mp
import time
import os

def add_values(value1, value2, value3):
    return value1 + value2 + value3

if __name__ == '__main__':
    inputs = []
    nums = []
    
    for i in range(1,4):
        nums.append(i)
    
    # pass in the list expanding out each item as a separate arg
    total = add_values(*nums)
    print(f'total={total}')
    
    
    # create a list of lists
    for _ in range(5):
        inputs.append(nums)
        
    print(f'inputs is now a list of 5 lists: {inputs}')
    
    pool = mp.Pool(processes=4)
    # use starmap to pass the list of lists
    outputs = pool.starmap(add_values, inputs)
    pool.close()
    pool.join()
    print(f'outputs={outputs}')