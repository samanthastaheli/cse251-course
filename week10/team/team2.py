"""
Course: CSE 251
Lesson Week: 10
File: team2.py
Author: Brother Comeau
Instructions:
- Look for the TODO comments
"""

from statistics import mode
import time
import threading
import mmap

# TEST FUNCTIONS --------------------------------------------------------------
def read_file(filename):
    with open(filename, mode='r', encoding='utf8') as file_obj:
        text = file_obj.read()
        print(text)

# -----------------------------------------------------------------------------
def reverse_file(filename):
    """ Display a file in reverse order using a mmap file. """
    # TODO add code here
    data =  open(filename, mode='r', encoding='utf8')

    for line in data:
        for word in line.split(' '):
            print(word)

def reverse_file_mmap(filename):
    """ Display a file in reverse order using a mmap file. """
    with open(filename, mode='r', encoding='utf8') as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as map_file:
        # if length is set to 0 it will do the full file but can be dangerous/problamatic if file is to big
            for line in iter(map_file.readline, 1):
                print(line)


# -----------------------------------------------------------------------------
def promote_letter_a(filename):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.
    """
    # TODO add code here
    pass


# -----------------------------------------------------------------------------
def promote_letter_a_threads(filename):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.

    Use N threads to process the file where each thread will be 1/N of the file.
    """
    # TODO add code here
    pass


# -----------------------------------------------------------------------------
def main():
    # read_file('data.txt')
    # reverse_file('data.txt')
    reverse_file_mmap('data.txt')
    # promote_letter_a('letter_a.txt')
    
    # TODO
    # When you get the function promote_letter_a() working
    #  1) Comment out the promote_letter_a() call
    #  2) run create_Data_file.py again to re-create the "letter_a.txt" file
    #  3) Uncomment the function below
    # promote_letter_a_threads('letter_a.txt')

if __name__ == '__main__':
    main()
