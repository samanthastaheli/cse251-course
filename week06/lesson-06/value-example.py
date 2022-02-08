from multiprocessing import Process, Value, Array
import ctypes

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]


if __name__ == '__main__':
    
    num = Value(ctypes.c_double)
    #num = Value('d', 0.0)
    
    arr = Array(ctypes.c_int, range(10))
    #arr = Array('i', range(10))

    p1 = Process(target=f, args=(num, arr))
    p1.start()
    p1.join()

    print(num.value)
    print(arr[:])

    print(*arr) # prints all items with a space in-between each and no brackets
    print(*arr, sep=", ") # prints all items with a comma in-between each and no brackets
