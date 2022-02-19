"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Samantha Staheli
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.

Submission Comment:
My program meets the requirements. I added comments throughout the code. 
In the main function I added an explanation of how many pipes are used and why.
"""

import random
import multiprocessing as mp
from multiprocessing import Value, Process
import os.path
import time

# Include cse 251 common Python files - Don't change
from cse251 import *
set_working_directory(__file__)

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'


# No Global variables

class Bag():
    """ bag of marbles - Don't change for the 93% """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change for the 93% """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', "Big Dip O'ruby", 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, parent_conn_creator, marble_count, delay):
        mp.Process.__init__(self)
        # Add any arguments and variables here
        self.parent_conn_creator = parent_conn_creator
        self.marble_count = marble_count # total amount of marbles to be made
        self.delay = delay

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for _ in range(self.marble_count):
            marble = random.choice(Marble_Creator.colors)
            self.parent_conn_creator.send(marble)

            time.sleep(self.delay)

        self.parent_conn_creator.send(None)

        self.parent_conn_creator.close()


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, child_conn_creator, parent_conn_bagger, bag_count, delay):
        mp.Process.__init__(self)
        # Add any arguments and variables here
        self.child_conn_creator = child_conn_creator
        self.parent_conn_bagger = parent_conn_bagger
        self.bag_count = bag_count # amount of marbles processed at once
        self.delay = delay
        self.bag = Bag()

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        while True: # this for loop with run until there is a return or break
            marble = self.child_conn_creator.recv()

            if(marble == None):
                self.parent_conn_bagger.send(None)
                self.child_conn_creator.close()
                self.parent_conn_bagger.close()
                return # while loop is broken because creator reached process amount 
        
            self.bag.add(marble)

            if(self.bag.get_size() == self.bag_count):
                self.parent_conn_bagger.send(self.bag)
                time.sleep(self.delay)

                self.bag = Bag()

class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, child_conn_bagger, parent_conn_assembler, delay):
        mp.Process.__init__(self)
        # Add any arguments and variables here
        self.child_conn_bagger = child_conn_bagger
        self.parent_conn_assembler = parent_conn_assembler
        self.delay = delay

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True: # this for loop with run until there is a return or break
            current_bag = self.child_conn_bagger.recv()

            if (current_bag == None):
                # last send to the bagger pipe is none as indicator process needs to end 
                # assembler aslo needs to end so none is sent
                # assembler and bagger now need to be closed
                self.parent_conn_assembler.send(None)
                self.child_conn_bagger.close()
                self.parent_conn_assembler.close()
                return # only thing that breaks the while loop
            
            large_marble = random.choice(Assembler.marble_names)

            # gift setup with 1 large marble and 7 other marbles
            gift = Gift(large_marble, current_bag)

            self.parent_conn_assembler.send(gift)


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, child_conn_assembler, gift_count):
        mp.Process.__init__(self)
        # Add any arguments and variables here
        self.child_conn_assembler = child_conn_assembler
        self.gift_count = gift_count

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        index = 0 # index is used to incease the gift count value 
        while True:
            wrap_gifts = self.child_conn_assembler.recv()

            with open(BOXES_FILENAME, 'a') as f: 
                if (wrap_gifts == None):
                    self.child_conn_assembler.close()
                    return
                else:
                    # here the asseblers pipe's contents are being appended to the txt file
                    f.write(wrap_gifts.__str__())
                    f.write('\n')
                    index += 1
                    self.gift_count.value = index


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function 

    Assembly Line (process/steps):
    The process of creating the gift can be compared to an assembly line because the process 
    is broken up into steps (creator, bagger, assembler, and wrapper).
    An assembly line also has materials, the materials for this process are the bag and gift classes.
    
    Pipe specifications: 
    The number of pipes depeneds on the number connections between the classes. In this case 
    there are 3 connections, so 3 pipes are required. These pipes are for creator, 
    bagger, and assembler. Wrapper does not need a pipe because is is the end of the process.
    """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count                = {settings[MARBLE_COUNT]}')
    log.write(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    log.write(f'settings["bag-count"]       = {settings[BAG_COUNT]}') 
    log.write(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    log.write(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    log.write(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')



    # create Pipes between creator -> bagger -> assembler -> wrapper
    # 3 pipes required
    parent_conn_creator, child_conn_creator = mp.Pipe()
    parent_conn_bagger, child_conn_bagger = mp.Pipe()
    parent_conn_assembler, child_conn_assembler = mp.Pipe()

    # create variable to be used to count the number of gifts
    gift_count = Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # pass the parent connector, child connector, an amount, and the delay 
    # to the classes that have pipes
    p_creator = Marble_Creator(parent_conn_creator, settings[MARBLE_COUNT], settings[CREATOR_DELAY])
    p_bagger = Bagger(child_conn_creator, parent_conn_bagger, settings[BAG_COUNT], settings[BAGGER_DELAY])
    p_assembler = Assembler(child_conn_bagger, parent_conn_assembler, settings[ASSEMBLER_DELAY])
    # pass assemblers child connector and gift count variable
    # wrapper does not have its own pipe because it is last in the assembly line of classes
    p_wrapper = Wrapper(child_conn_assembler, gift_count)

    log.write('Starting the processes')
    p_creator.start()
    p_bagger.start()
    p_assembler.start()
    p_wrapper.start()

    log.write('Waiting for processes to finish')
    p_creator.join()
    p_bagger.join()
    p_assembler.join()
    p_wrapper.join()

    display_final_boxes(BOXES_FILENAME, log)

    # Log the number of gifts created.
    log.stop_timer(f'Total time to transfer content = {gift_count.value}: ')



if __name__ == '__main__':
    main()

