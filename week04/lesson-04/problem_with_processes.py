import multiprocessing as mp


def process_function(process_id, data):
    # only change the value based on process_id
    for i in range(10):
        data[process_id] += 1
    print(f'Process {process_id}: {data}')


def main():
    # Create a value with each thread
    data = [0] * 3

    # Create 3 processes, pass a "process_id" for each thread
    processes = [mp.Process(target=process_function, args=(i, data))
                 for i in range(3)]

    for i in range(3):
        processes[i].start()

    for i in range(3):
        processes[i].join()

    print(f'All work completed: {sum(data)}')


if __name__ == '__main__':
    main()