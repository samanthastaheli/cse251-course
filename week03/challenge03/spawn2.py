import multiprocessing as mp
import time

def func():
      name = mp.current_process().name
      time.sleep(0.5)
      print(f'called function in process: {name}')
      return

if __name__ == '__main__':
      jobs = []
      for _ in range(5):
            p = mp.Process(target=func)
            
            # means the process will end when parent ends
            # and it can't spawn child processes of its own
            #p.daemon = True 
            jobs.append(p)
      
      for j in jobs:
            j.start()
            j.join()