import multiprocessing
import time
import os

class MyProcess(multiprocessing.Process):
      def run(self):
            print(f'run method called in process {self}, pid={os.getpid()}')

print(f'__name__={__name__}')

if __name__ == '__main__':
    for _ in range(5):
        p = MyProcess()
        p.start()
        p.join()