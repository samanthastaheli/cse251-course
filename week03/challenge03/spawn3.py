import multiprocessing
import time

def func():
      name = multiprocessing.current_process().name
      print(f'called function in process: {name}')
      time.sleep(0.5)
      print(f'finished function: {name}')
      return

if __name__ == '__main__':
      p = multiprocessing.Process(target=func)
      
      print(f'about to execute {p}, is alive = {p.is_alive()}')
      p.start()
      print(f'executing {p}, is alive = {p.is_alive()}')
      
      p.terminate()
      while p.is_alive():
            print(f'{p} terminated but waiting, is alive = {p.is_alive()}')
            
      p.join()
      print(f'{p} joined, is alive = {p.is_alive()}')
      print(f'{p} exit code = {p.exitcode}')
      