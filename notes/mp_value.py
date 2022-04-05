from multiprocessing import Manager
import multiprocessing as mp

def increase_number(number):
    number += 1
def main():
    manage = Manager()
    test_number = manage.Value(0)

    print(f'start num: {test_number}')

    test_process = mp.Process(target=increase_number, args=(test_number))

    test_process.start()
    test_process.join()

    print(f'end num: {test_number}')

if __name__ == ("__main__"):
    main()