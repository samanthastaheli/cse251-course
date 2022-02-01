"""
------------------------------------------------------------------------------
Course: CSE 251
Lesson Week: 03
File: assignment.py
Author: <Your Name>

Purpose: Video Frame Processing

Instructions:

- Follow the instructions found in Canvas for this assignment
- No other packages or modules are allowed to be used in this assignment.
  Do not change any of the from and import statements.
- Only process the given MP4 files for this assignment

------------------------------------------------------------------------------
"""

from tkinter.tix import FileSelectBox
from matplotlib.pylab import plt  # load plot library
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

# 4 more than the number of cpu's on your computer
CPU_COUNT = mp.cpu_count() + 4  

# TODO Your final video need to have 300 processed frames.  However, while you are 
# testing your code, set this much lower
FRAME_COUNT = 300
num_processes = 2
RED   = 0
GREEN = 1
BLUE  = 2


def create_new_frame(image_file, green_file, process_file):
    """ Creates a new image file from image_file and green_file """

    # this print() statement is there to help see which frame is being processed
    print(f'{process_file[-7:-4]}', end=',', flush=True)

    image_img = Image.open(image_file)
    green_img = Image.open(green_file)

    # Make Numpy array
    np_img = np.array(green_img)

    # Mask pixels 
    mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

    # Create mask image
    mask_img = Image.fromarray((mask*255).astype(np.uint8))

    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(process_file)


# TODO add any functions to need here
def call_create_frame(files):
    arg1 = files[0]
    arg2 = files[1]
    arg3 = files[2]
    create_new_frame(arg1, arg2, arg3)

def create_list():
  files = []
  for i in range(1, FRAME_COUNT+1, 1):
    image = rf'elephant/image{i:03d}.png'
    green = rf'green/image{i:03d}.png'
    process = rf'processed/image{i:03d}.png'
    t = (image, green, process)
    files.append(t)
  return files

if __name__ == '__main__':
    # single_file_processing(300)
    # print('cpu_count() =', cpu_count())

    all_process_time = timeit.default_timer()
    log = Log(show_terminal=True)

    xaxis_cpus = []
    yaxis_times = []

    # TODO Process all frames trying 1 cpu, then 2, then 3, ... to CPU_COUNT add results to xaxis_cpus and yaxis_times

    start_time = timeit.default_timer()
    files_list = create_list()

    for i in range(1,CPU_COUNT+1):
      process_time = timeit.default_timer()
      with mp.Pool(i) as p:
        p.map(call_create_frame, files_list)
        log.write(f'Time for {FRAME_COUNT} frames using {i} processes:{timeit.default_timer() - process_time}')  
      yaxis_times.append(timeit.default_timer() - process_time)
      xaxis_cpus.append(i)

    log.write(f'Total Time for ALL processing: {timeit.default_timer() - all_process_time}')

    # create plot of results and also save it to a PNG file
    plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')
    
    plt.title('CPU Core yaxis_times VS CPUs')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
    plt.show()
