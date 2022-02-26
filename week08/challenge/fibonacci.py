import threading
import string

'''
Fibonacci is the sum of 2 previous numbers.
0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, ...
base case: 0 or 1

number is how many numbers to process
'''

def fibonacci(number):
    if (number in [0, 1]): # same as (number == 0 or number == 1)
        return number
    else:
        first = fibonacci(number - 1)
        second = fibonacci(number - 2)
        total = first + second
        print(f'{first=} + {second=} = {total}')
        return total

if __name__ == '__main__':
    value = fibonacci(10)
    print(f'{value=}')
    assert(value == 55)
