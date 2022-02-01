import time
import threading
import os
import shutil
import random
import string
from pathlib import Path

TEMP_DIR = 'temp'
DIR1 = 'dirA-M'
DIR2 = 'dirN-Z'

# ----------------------------------------------------------------------------
# Create directory, if necessary
# ----------------------------------------------------------------------------
def create_directories(directory):
      if not os.path.exists(directory):
            os.makedirs(directory)

# ----------------------------------------------------------------------------
# Create the directories and files
# ----------------------------------------------------------------------------
class Create_Files_Thread(threading.Thread):
      
      def __init__(self, lock):
            # always call the super when exending another class
            super().__init__()
            self.lock = lock
            
      def run(self):
            # join the current working directory (cwd) with the new directory
            # to get the full path to the temp directory
            full_path = os.path.join(os.getcwd(), TEMP_DIR)
            
            # create 10 files inside of temp directory with random letter as name
            letters = list(string.ascii_lowercase) # windows is not case-sensitive, so only use lowercase
            for i in range(10):
                  name = letters.pop(random.randrange(len(letters)))
                  filename = (f'{full_path}/{name}.txt')
                  print(f'creating {filename}')
                  with self.lock:
                        with open(filename, 'w') as fp:
                              for _ in range(1000000):
                                    fp.write(f'{string.ascii_letters}\n')
            
            print("thread done creating files")

# ----------------------------------------------------------------------------
# A Thread class to move a file from one directory to another
# ----------------------------------------------------------------------------
class Move_Files_Thread(threading.Thread):
      
      def __init__(self, lock: threading.Lock, stop: threading.Lock):
            # always call the super when exending another class
            super().__init__()
            self.lock = lock
            self.stop = stop
            
      def run(self):
            
            # We will sit in a loop waiting for a file to get created
            while True:
                  
                  # It's good to sleep a bit while polling (endlessly looping)
                  time.sleep(0.1) 
                  
                  files = os.listdir(TEMP_DIR)
                  
                  # only lock if there are files to move
                  if(files):
                        with self.lock:
                              for file in files:
                                    full_path = os.path.join(TEMP_DIR, file)
                                    if(os.path.isfile(full_path)):
                                          name = Path(file).stem
                                          if(ord(name[0].lower()) < ord('n')):
                                                shutil.move(full_path, DIR1)
                                          else:
                                                shutil.move(full_path, DIR2)
                  else:
                        # if stop is locked it means no more files will be created
                        if(self.stop.locked()):
                              return
                              
                        
# ----------------------------------------------------------------------------
def main():
      
      # print(f'get the current working directory (cwd): {os.getcwd()}')
      # print(f'list out all the files and directories in a directory: {os.listdir()}')
      # print(f'os.path.isfile(file) will return true if file is a file and not a directory')
      # print('shutil.move(src, dest) moves a file from src to dest')
      # print('os.makedirs(dir) creates a directory in the working directory')
      # print('os.path.exists(dir) returns true if the dir exists')
      # print('os.path.join(working_dir, dir) joins the dir directory with the working directory, this is useful if you need to absolute path to a directory')
      # print('Path(path).stem will give you the filename in the path without the extension')
      # print('ord(char) will give you the ASCII value of a character')
    
      create_directories(DIR1)
      create_directories(DIR2)
      create_directories(TEMP_DIR)
      
      # TODO - create a lock
      lock = threading.Lock()
      stop = threading.Lock()
      
      # TODO - create a move thread
      move_thread = Move_Files_Thread(lock, stop)
      
      # TODO - create a create thread
      create_thread = Create_Files_Thread(lock)
      
      # TODO - start each thread
      move_thread.start()
      create_thread.start()
      
      # TODO - join each thread 
      create_thread.join()
      stop.acquire()
      move_thread.join()

if __name__ == '__main__':
    main()