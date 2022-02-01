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
NUM_FILES = 10
NUM_LINES_PER_FILE = 1000000

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
            # TODO join the current working directory (cwd) with the new directory
            # to get the full path to the temp directory
            #full_path = 
            
            # TODO create a list of all lowercase letters (Windows is not case-sensitive, so only use lowercase)
            #letters = 
            for i in range(NUM_FILES):
                  
                  # TODO get and remove a random letter from the letters list
                  #char = 
                  
                  # TODO set the filename by concatenating the full_path with the char plus '.txt'
                  filename = ""
                  print(f'creating {filename}')
                  
                  # TODO lock, open file, and loop NUM_LINES_PER_FILE times writing 'string.ascii_letter\n'
            
            print("thread done creating files")

# ----------------------------------------------------------------------------
# A Thread class to move a file from one directory to another
# ----------------------------------------------------------------------------
class Move_Files_Thread(threading.Thread):
      
      def __init__(self, lock: threading.Lock):
            # always call the super when exending another class
            super().__init__()
            self.lock = lock
            
      def run(self):
            
            # We will sit in a loop waiting for a file to get created
            while True:
                  
                  # It's good to sleep a bit while polling (endlessly looping)
                  time.sleep(0.1) 
                  
                  # TODO get all the files in the TEMP_DIR
                  files = threading.get
                  
                  # TODO lock, loop over each file, get the full path to the file,
                  # decide if the file should go into A-M or N-Z, then move the 
                  # file to the appropriate directory
                  
                  # You might not have a way to know when to stop looping...you'll
                  # need to kill the process to end the program.
                              
                        
# ----------------------------------------------------------------------------
def main():
      
      print(f'get the current working directory (cwd): {os.getcwd()}')
      print(f'list out all the files and directories in a directory: {os.listdir()}')
      print(f'os.path.isfile(file) will return true if file is a file and not a directory')
      print('shutil.move(src, dest) moves a file from src to dest')
      print('os.makedirs(dir) creates a directory in the working directory')
      print('os.path.exists(dir) returns true if the dir exists')
      print('os.path.join(working_dir, dir) joins the dir directory with the working directory, this is useful if you need to absolute path to a directory')
      print('Path(path).stem will give you the filename in the path without the extension')
      print('ord(char) will give you the ASCII value of a character')
      print(f'string.ascii_lowercase={string.ascii_lowercase}')
      print(f'string.ascii_lowercase={string.ascii_letters}')
      print('To write to a file use: with open(filename, "w") as fp:   and then fp.write("text to write"')
    
      create_directories(DIR1)
      create_directories(DIR2)
      create_directories(TEMP_DIR)
      
      # TODO create a lock
      lock = threading.Lock()
      
      # TODO - create a move thread
      move_thread = Move_Files_Thread()
      
      # TODO - create a create thread
      create_thread = Create_Files_Thread()
      
      # TODO - start each thread
      move_thread.start()
      create_thread.start()
      
      # TODO - join each thread 
      move_thread.join()
      create_thread.join()

if __name__ == '__main__':
    main()