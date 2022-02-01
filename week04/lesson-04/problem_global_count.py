import threading

VALUES_TO_ADD = 1000
count = 0


def thread_function(thread_id):
    global count
    # Only change the value in the list based on thread_id
    for i in range(VALUES_TO_ADD):
        count += 1
    print(f'Process {thread_id}: {count}')


def main():
    global count

    lock = threading.Lock()

    # Create 3 threads, pass a "thread_id" for each thread
    threads = [threading.Thread(target=thread_function, args=(i,))
               for i in range(3)]

    for i in range(3):
        threads[i].start()

    for i in range(3):
        threads[i].join()

    print(f'All work completed: {count}')


if __name__ == '__main__':
    main()
