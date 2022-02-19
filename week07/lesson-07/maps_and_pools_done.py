import multiprocessing as mp

from cse251 import *
set_working_directory(__file__)

# Global result list
result_list = []


def square_me(number):
    print(f'{mp.current_process()}\n')
    return number * number


def callback_function(result):
    result_list.append(result)


def apply_async_with_callback():

    numbers = []
    for n in range(101):
        numbers.append(n)

    # TODO using pool.apply, get results after calling call_me. Apply is (was?)
    # used when you had arbitray arguments to a function (meaning you didn't
    # know how many arguments were going to be passed in). Not really used anymore.
    pool = mp.Pool(4)
    result = pool.apply(square_me, args=(10,))
    print("here")
    pool.close()
    pool.join()
    print(f'pool.apply:\n{result}\n')

    # MAP - Functional Programming: functions don't modify the input parameters
    # (i.e., nothing is passed by reference/object, only value),
    # and the state the program is not changed. Only a result of the function
    # is returned.
    # NOTE: the map function returns a map object, which is an iterator. So,
    # to print out the results as a list, you need to cast results as a list

    # NON-PARALLEL
    # get the results after mapping (apply) a function to a list of numbers.
    result = map(square_me, numbers)
    print(f'map:\n{list(result)}\n')

    # PARALLEL
    # get the results after mapping (apply) a function to a list of numbers
    # using a process pool
    pool = mp.Pool(5)
    result =  pool.map(square_me, numbers)
    pool.close()
    pool.join()
    print(f'pool.map:\n{list(result)}\n')

    # PARALLEL
    # TODO get the results after mapping (apply) a function to a list of numbers
    # using a process pool (using the context manager 'with')
    with mp.Pool(5) as p:
        result = p.map(square_me, numbers)
    print(f'pool.map (using with):\n{list(result)}\n')

    # get the results using 'apply_async'.
    # Use apply_async when you need to pass non-iterable values to a function
    pool = mp.Pool(5)
    results = list(pool.apply_async(square_me, args=(i,)) for i in range(101))
    print("here 1")
    output = [r.get() for r in results]
    print("here 2")
    pool.close()
    pool.join()
    print(f'pool.apply_async:\n{output}\n')

    # get the results using 'apply_async' with callback
    pool = mp.Pool(5)
    for i in range(101):
        pool.apply_async(square_me, args=(i,), callback=callback_function)
    pool.close()
    pool.join()
    print(f'pool.apply_async (with callback):\n{result_list}\n')

    #  Combine map and async. Normal map function is blocking,
    # but map_async is non-blocking
    pool = mp.Pool(5)
    result = pool.map_async(square_me, numbers)
    print('before waiting')
    result.wait()
    print('after waiting')
    pool.close()
    pool.join()
    print(f'pool.map_async:\n{result.get()}\n')


if __name__ == '__main__':
    apply_async_with_callback()
