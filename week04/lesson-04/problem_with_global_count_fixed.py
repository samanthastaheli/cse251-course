import threading

VALUES_TO_ADD = 1000


def thread_function(thread_id, data):
    # Only change the value in the list based on thread_id
    for i in range(VALUES_TO_ADD):
        data[thread_id] += 1
    print(f'Thread {thread_id}: {data}')


def main():
    # Create a value with each thread
    data = [0] * 3

    # Create 3 threads, pass a "thread_id" for each thread
    threads = [threading.Thread(
        target=thread_function, args=(i, data)) for i in range(3)]

    for i in range(3):
        threads[i].start()

    for i in range(3):
        threads[i].join()

    print(f'All work completed: {sum(data)}')


if __name__ == '__main__':
    main()
