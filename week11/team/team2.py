"""
Course: CSE 251
Lesson Week: 11
File: team2.py
Author: Brother Comeau

Purpose: Team Activity 2: Queue, Pipe, Stack

Instructions:

Part 1:
- Create classes for Queue_t, Pipe_t and Stack_t that are thread safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple threads.

Part 2
- Create classes for Queue_p, Pipe_p and Stack_p that are process safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple processes.

Queue methods:
    - constructor(<no arguments>)
    - size()
    - get()
    - put(item)

Stack methods:
    - constructor(<no arguments>)
    - push(item)
    - pop()

Steps:
1) write the Queue_t and test it with threads.
2) write the Queue_p and test it with processes.
3) Implement Stack_t and test it 
4) Implement Stack_p and test it 

Note: Testing means having lots of concurrency/parallelism happening.  Also
some methods for lists are thread safe - some are not.

"""
import time
import threading
import multiprocessing as mp

# -------------------------------------------------------------------
class Queue_t:
    '''
    creates a queue 
    uses threads to append and delete from queue
    '''
    def __init__(self):
        self.queue_list = []

    def put(self, item):
        self.queue_list.append(item) 

    def get(self):
        # pop will remove first item in list when 
        return self.queue_list.pop(0) 
    
    def size(self):
        return len(self.queue_list)


# -------------------------------------------------------------------
class Stack_t:
    '''
    creates a stack 
    uses threads to append and delete from stack
    '''
    def __init__(self):
        self.stack_list = []

    def push(self, item):
        self.stack_list.push(item) 

    def pop(self):
        return self.stack_list.pop() 
    
    def size(self):
        return len(self.stack_list)

# -------------------------------------------------------------------
class Queue_p:
    # create a queue using pipes
	pass

# -------------------------------------------------------------------
class Stack_p:
    # create a stack using pipes
	pass


# TESTS -------------------------------------------------------------

def queue_t_test(thread_num, amount, queue, list):
    '''
    add numbers to list
    return length of list and first and last values added
    '''
    for i in range(amount):
        item = i+1
        queue.put(item)
        print(f'thread num {thread_num} adding {item} to queue_t')
    print(f'thread num {thread_num} len: {queue.size()}, first: {list[0]}, last: {list[i]}')

def stack_t_test(thread_num, amount, stack, list):
    '''
    add numbers to list
    return length of list and first and last values added
    '''
    for i in range(amount):
        item = i+1
        stack.push(item)
        print(f'thread num {thread_num} adding {item} to stack_t')
    print(f'thread num {thread_num} len: {stack.size()}, first: {list[0]}, last: {list[i]}')
    
# -------------------------------------------------------------------

def main():
    num = 20

    queue_t = Queue_t()
    queue_list = queue_t.queue_list

    t1 = threading.Thread(target=queue_t_test, args=(1, num, queue_t, queue_list))
    t2 = threading.Thread(target=queue_t_test, args=(2, num, queue_t, queue_list))

    stack_t = Stack_t()
    stack_list = stack_t.stack_list

    t3 = threading.Thread(target=stack_t_test, args=(1, num, stack_t, stack_list))
    t4 = threading.Thread(target=stack_t_test, args=(2, num, stack_t, stack_list))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

if __name__ == '__main__':
    main()
