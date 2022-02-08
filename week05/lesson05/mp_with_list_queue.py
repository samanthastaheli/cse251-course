import multiprocessing


def process_function(data, q):
    for d in data:
        q.put(d)


def main():

    # Create a mp list
    data_list = multiprocessing.Manager().list()

    # Add dummy values to list
    for i in range(4):
        data_list.append(i)

    # Create a mp queue
    data_queue = multiprocessing.Manager().Queue()

    # Create process to add all number in list to queue
    p = multiprocessing.Process(
        target=process_function, args=(data_list, data_queue))

    p.start()
    p.join()

    # put None at end of queue to stop it when iterating to find sum
    data_queue.put(None)

    total = 0
    for item in iter(data_queue.get, None):
        total += item

    print(f'All work completed: sum = {total}')


if __name__ == '__main__':
    main()
