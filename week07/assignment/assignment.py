"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: <Your name here>
Purpose: Process Task Files
Instructions:  See I-Learn

submisson comment:
My code meets requirements. 

pool sizes used: 
    primes = 10
    words = 10
    upper = 5
    sum = 5
    names = 15

To determine the best pool sizes I tested each function individually to find 
how long each function takes. The results were:
    pool size 1:
        primes = 0.7679446 sec
        words = 0.7831659 sec
        upper = 0.7072219 sec
        sum = 0.7612405 sec 
        names = 3.1642854 sec
    pool size 5:
        primes = 0.9600511 sec
        words = 1.0587852 sec
        upper = 0.967607 sec
        sum = 0.9916522 sec
        names = 3.4720493 sec
I set names pool size to be the largest and sums the smallest based on the 
results showing that the most time consuming task is names and least is sums.
Primes and words time are in the middle of the tasks, so their pool size was 
also in the middle. I tested many values based on these conditions and found 
that 5, 10, and 15 to be the fastest.
"""

from datetime import datetime, timedelta
from subprocess import call
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *
set_working_directory(__file__)

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
 
def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value) == True:
        return (f'{value} is prime')
    else:
        return (f'{value} is not prime')

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    file = open('words.txt', 'r')
    if word in file:
        return (f'{word} Found')
    else:
        return (f'{word} not found')

def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    uppercase = text.upper()
    return (f'{text} ==>  uppercase version of {uppercase}')


def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    total = 0

    for num in range(start_value, end_value, 1):
        total += num
    
    return (f'sum of {start_value:,} to {end_value:,} = {total:,}')

def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        name = data['name']
        return (f'{url} has name {name}')
    else:
        return (f'{url} had an error receiving the information')
        
# callback functions
def callback_primes(value):
    global result_primes
    result_primes.append(value)

def callback_words(value):
    global result_words
    result_words.append(value)

def callback_upper(value):
    global result_upper
    result_upper.append(value)

def callback_sums(value):
    global result_sums
    result_sums.append(value)

def callback_name(value):
    global result_names
    result_names.append(value)

def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # Create process pools
    # 5 tasks: task_primes, task_words, task_upper, task_sums, task_names
    pool_primes = mp.Pool(10)
    pool_words = mp.Pool(10)
    pool_upper = mp.Pool(5)
    pool_sum = mp.Pool(5)
    pool_url = mp.Pool(15)

    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            pool_primes.apply_async(task_prime, args=(task['value'],), callback = callback_primes)
            # task_prime(task['value'])
        elif task_type == TYPE_WORD:
            pool_words.apply_async(task_word, args=(task['word'],), callback = callback_words)
            # task_word(task['word'])
        elif task_type == TYPE_UPPER:
            pool_upper.apply_async(task_upper, args=(task['text'],), callback = callback_upper)
            # task_upper(task['text'])
        elif task_type == TYPE_SUM:
            pool_sum.apply_async(task_sum, args=(task['start'], task['end']), callback=callback_sums)
            # task_sum(task['start'], task['end'])
        elif task_type == TYPE_NAME:
            pool_url.apply_async(task_name, args=(task['url'],), callback=callback_name)
            # task_name(task['url'])
        else:
            log.write(f'Error: unknown task type {task_type}')


    # start and wait pools
    pool_primes.close()
    pool_words.close()
    pool_upper.close()
    pool_sum.close()
    pool_url.close()

    pool_primes.join()
    pool_words.join()
    pool_upper.join()
    pool_sum.join()
    pool_url.join()

    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Primes: {len(result_primes)}')
    log.write(f'Words: {len(result_words)}')
    log.write(f'Uppercase: {len(result_upper)}')
    log.write(f'Sums: {len(result_sums)}')
    log.write(f'Names: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

    log.write(f'Pool Amount Primes: {pool_primes}')
    log.write(f'Pool Amount Words: {pool_words}')
    log.write(f'Pool Amount Uppercase: {pool_upper}')
    log.write(f'Pool Amount Sums: {pool_sum}')
    log.write(f'Pool Amount Names: {pool_url}')

if __name__ == '__main__':
    main()