import multiprocessing

def func(argument):
      
      print(f'called function in process: {argument}')
      return

if __name__ == '__main__':
    for i in range(5):
        p = multiprocessing.Process(target=func, args=(i,))
        p.start()
        p.join()