"""
Course: CSE 251
Lesson Week: 14
File: assignment.py
Author: Samantha Staheli
Purpose: Assignment 13 - Family Search

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
family = Request_thread(f'{TOP_API_URL}/family/{id}')

Requesting an individual from the server:
person = Request_thread(f'{TOP_API_URL}/person/{id}')


Describe how to speed up part 1:

To speed up part 1 I created threads for the husband 
and wife. Then created threads for each of their children. 
These new threads recursively called the function and passes 
in the childs family id so their spouse and children 
would be added to the tree.


Describe how to speed up part 2:

To speed up part 2 you need to add a familys generation of 
children to the tree concurrently with another family. This is 
done by creating a thread for every child. This created a 
level order traversal by traversing through the level of 
children first then traversing through the next level. 
I created a thread for each child because their next level 
will be different than their siblings. This speed up the 
process because every child is adding their children to the 
tree making them concurrent with their other siblings.


10% Bonus to speed up part 3:

Part 3 is similar to part 2, so it would be sped up 
the same way but semaphores would be incorporated.

"""
from concurrent.futures import thread
import time
import threading
import multiprocessing as mp
import json
import random
from turtle import done
import requests

# Include cse 251 common Python files - Dont change
from cse251 import *
set_working_directory(__file__)


TOP_API_URL = 'http://127.0.0.1:8123'
DONE = False

# ----------------------------------------------------------------------------
# Do not change this class
class Person:

    def __init__(self, data):
        super().__init__()
        self.id = data['id']
        self.name = data['name']
        self.parents = data['parent_id']
        self.family = data['family_id']
        self.birth = data['birth']

    def __str__(self):
        output  = f'id        : {self.id}\n'
        output += f'name      : {self.name}\n'
        output += f'birth     : {self.birth}\n'
        output += f'parent id : {self.parents}\n'
        output += f'family id : {self.family}\n'
        return output

# ----------------------------------------------------------------------------
# Do not change this class
class Family:

    def __init__(self, id, data):
        super().__init__()
        self.id = data['id']
        self.husband = data['husband_id']
        self.wife = data['wife_id']
        self.children = data['children']

    def children_count(self):
        return len(self.children)

    def __str__(self):
        output  = f'id         : {self.id}\n'
        output += f'husband    : {self.husband}\n'
        output += f'wife       : {self.wife}\n'
        for id in self.children:
            output += f'  Child    : {id}\n'
        return output

# -----------------------------------------------------------------------------
# Do not change this class
class Tree:

    def __init__(self, start_family_id):
        super().__init__()
        self.people = {}
        self.families = {}
        self.start_family_id = start_family_id

    def add_person(self, person):
        if self.does_person_exist(person.id):
            print(f'ERROR: Person with ID = {person.id} Already exists in the tree')
        else:
            self.people[person.id] = person

    def add_family(self, family):
        if self.does_family_exist(family.id):
            print(f'ERROR: Family with ID = {family.id} Already exists in the tree')
        else:
            self.families[family.id] = family

    def get_person(self, id):
        if id in self.people:
            return self.people[id]
        else:
            return None

    def get_family(self, id):
        if id in self.families:
            return self.families[id]
        else:
            return None

    def get_person_count(self):
        return len(self.people)

    def get_family_count(self):
        return len(self.families)

    def does_person_exist(self, id):
        return id in self.people

    def does_family_exist(self, id):
        return id in self.families

    def display(self, log):
        log.write('*' * 60)
        log.write('Tree Display')
        for family_id in self.families:
            fam = self.families[family_id]

            log.write(f'Family id: {family_id}')

            # Husband
            husband = self.get_person(fam.husband)
            if husband == None:
                log.write(f'  Husband: None')
            else:
                log.write(f'  Husband: {husband.name}, {husband.birth}')

            # wife
            wife = self.get_person(fam.wife)
            if wife == None:
                log.write(f'  Wife: None')
            else:
                log.write(f'  Wife: {wife.name}, {wife.birth}')

            # Parents of Husband
            if husband == None:
                log.write(f'  Husband Parents: None')
            else:
                parent_fam_id = husband.parents
                if parent_fam_id in self.families:
                    parent_fam = self.get_family(parent_fam_id)
                    father = self.get_person(parent_fam.husband)
                    mother = self.get_person(parent_fam.wife)
                    log.write(f'  Husband Parents: {father.name} and {mother.name}')
                else:
                    log.write(f'  Husband Parents: None')

            # Parents of Wife
            if wife == None:
                log.write(f'  Wife Parents: None')
            else:
                parent_fam_id = wife.parents
                if parent_fam_id in self.families:
                    parent_fam = self.get_family(parent_fam_id)
                    father = self.get_person(parent_fam.husband)
                    mother = self.get_person(parent_fam.wife)
                    log.write(f'  Wife Parents: {father.name} and {mother.name}')
                else:
                    log.write(f'  Wife Parents: None')

            # children
            output = []
            for index, child_id in enumerate(fam.children):
                person = self.people[child_id]
                output.append(f'{person.name}')
            out_str = str(output).replace("'", '', 100)
            log.write(f'  Children: {out_str[1:-1]}')


    def _test_number_connected_to_start(self):
        # start with first family, how many connected to that family
        inds_seen = set()

        def _recurive(family_id):
            nonlocal inds_seen
            if family_id in self.families:
                # count people in this family
                fam = self.families[family_id]

                husband = self.get_person(fam.husband)
                if husband != None:
                    if husband.id not in inds_seen:
                        inds_seen.add(husband.id)
                    _recurive(husband.parents)
                
                wife = self.get_person(fam.wife)
                if wife != None:
                    if wife.id not in inds_seen:
                        inds_seen.add(wife.id)
                    _recurive(wife.parents)

                for child_id in fam.children:
                    if child_id not in inds_seen:
                        inds_seen.add(child_id)


        _recurive(self.start_family_id)
        return len(inds_seen)


    def _count_generations(self, family_id):
        max_gen = -1

        def _recurive_gen(id, gen):
            nonlocal max_gen
            if id in self.families:
                if max_gen < gen:
                    max_gen = gen

                fam = self.families[id]

                husband = self.get_person(fam.husband)
                if husband != None:
                    _recurive_gen(husband.parents, gen + 1)
                
                wife = self.get_person(fam.wife)
                if wife != None:
                    _recurive_gen(wife.parents, gen + 1)

        _recurive_gen(family_id, 0)
        return max_gen + 1

    def __str__(self):
        out = '\nTree Stats:\n'
        out += f'Number of people                    : {len(self.people)}\n'
        out += f'Number of families                  : {len(self.families)}\n'
        out += f'Max generations                     : {self._count_generations(self.start_family_id)}\n'
        out += f'People connected to starting family : {self._test_number_connected_to_start()}\n'
        return out


# ----------------------------------------------------------------------------
# Do not change
class Request_thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)


# -----------------------------------------------------------------------------
# TODO - Change this function to speed it up.  Your goal is to create the complete
#        tree faster.
def depth_fs_pedigree(family_id, tree):
    """
    outline:

    request family information
    request Husband - add to tree (Note there might not a husband in the family)
    request wife - add to tree (Note there might not a wife in the family)
    request children - add them to tree
    recursive call on the husband
    recursive call on the wife
    """
    if family_id == None:
        return
    print(f'Retrieving Family: {family_id}')
    
    # get fam data
    startingFamData = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    startingFamData.start()
    startingFamData.join()

    famObject = Family(family_id, startingFamData.response)
    # add family to family tree
    tree.add_family(famObject)

    husReq = Request_thread(f'{TOP_API_URL}/person/{famObject.husband}')
    wifReq = Request_thread(f'{TOP_API_URL}/person/{famObject.wife}')
    husReq.start()
    husReq.join()

    wifReq.start()
    wifReq.join()

    husband = Person(husReq.response)
    tree.add_person(husband)
    print(f'Added husband: {husband} Person Count now: {tree.get_person_count()}')

    wife = Person(wifReq.response)
    tree.add_person(wife)
    print(f'Added wife: {wife} Person Count now: {tree.get_person_count()}')


    print(f'family object: {famObject}')

    for childId in famObject.children:
        personRequest = Request_thread(f'{TOP_API_URL}/person/{childId}')
        personRequest.start()
        personRequest.join()
        child = Person(personRequest.response)
        tree.add_person(child)
        print(f'Added child: {child} Person Count now: {tree.get_person_count()}')

    threads_list = []

    if husband.parents != None:
        # depth_fs_pedigree(husband.parents, tree)
        husband_thread = threading.Thread(target=depth_fs_pedigree, args=(husband.parents, tree,))
        threads_list.append(husband_thread)

    if wife.parents != None:
        # depth_fs_pedigree(wife.parents, tree)
        wife_thread = threading.Thread(target=depth_fs_pedigree, args=(wife.parents, tree,))
        threads_list.append(wife_thread)

    if len(threads_list) >= 0:
        for threads in threads_list:
            threads.start()
            
        for threads in threads_list:
            threads.join()

    
# -----------------------------------------------------------------------------
# You must not change this function
def part1(log, start_id, generations):
    tree = Tree(start_id)

    req = Request_thread(f'{TOP_API_URL}/start/{generations}')
    req.start()
    req.join()

    log.start_timer('Depth-First')
  
    depth_fs_pedigree(start_id, tree)
    total_time = log.stop_timer()


    req = Request_thread(f'{TOP_API_URL}/end')
    req.start()
    req.join()

    tree.display(log)
    log.write(tree)
    log.write(f'total_time                   : {total_time}')
    log.write(f'People and families / second : {(tree.get_person_count()  + tree.get_family_count()) / total_time}')
    log.write('')
    
# -----------------------------------------------------------------------------
def breadth_fs_pedigree(start_id, tree):
    # implement breadth first retrieval
    # This video might help understand BFS
    # https://www.youtube.com/watch?v=86g8jAQug04

    # print(f'Retrieving Family: {start_id}')

    if start_id == None:
        return

    # if start_id is already in the tree then return
    if tree.does_family_exist(start_id):
        return

    # get fam data
    famData = Request_thread(f'{TOP_API_URL}/family/{start_id}')
    famData.start()
    famData.join()

    # add family to family tree
    famObject = Family(start_id, famData.response)
    tree.add_family(famObject)
    print(f'family object: {famObject}')

    # if family does not have children return
    if len(famObject.children) == 0:
        return

    # get husband and wife data
    husReq = Request_thread(f'{TOP_API_URL}/person/{famObject.husband}')
    wifReq = Request_thread(f'{TOP_API_URL}/person/{famObject.wife}')

    husReq.start()
    husReq.join()

    wifReq.start()
    wifReq.join()

    # add husband and wife to tree
    husband = Person(husReq.response)
    tree.add_person(husband)
    print(f'Added husband: {husband.id}')
    print(f'Person Count now: {tree.get_person_count()}')

    wife = Person(wifReq.response)
    tree.add_person(wife)
    print(f'Added wife: {wife.id}')
    print(f'Person Count now: {tree.get_person_count()}')

    # start thread for every child
    children_list = []
    children_threads = []
    for childId in famObject.children:
        # get child data
        childRequest = Request_thread(f'{TOP_API_URL}/person/{childId}')
        childRequest.start()
        childRequest.join()
        # add child to tree
        child = Person(childRequest.response)
        tree.add_person(child)
        # add the child to the children_list
        # if child.family is not None:
        children_list.append(child)
        print(f'Added child: {child.id}')
        print(f'Person Count now: {tree.get_person_count()}')

        # children_threads.append(threading.Thread(target=breadth_fs_pedigree, args=(child.id, tree,)))

    

    # start threads for each child
    for child in children_list:
        print(f'starting thread for child: {child.id}')
        children_threads.append(threading.Thread(target=breadth_fs_pedigree, args=(child.id, tree,)))

    if len(children_threads) >= 0:
        for threads in children_threads:
            threads.start()
            
        for threads in children_threads:
            threads.join()


# -----------------------------------------------------------------------------
# You must not change this function
def part2(log, start_id, generations):
    tree = Tree(start_id)

    req = Request_thread(f'{TOP_API_URL}/start/{generations}')
    req.start()
    req.join()

    log.start_timer('Breadth-First')
    breadth_fs_pedigree(start_id, tree)
    total_time = log.stop_timer()

    req = Request_thread(f'{TOP_API_URL}/end')
    req.start()
    req.join()

    tree.display(log)
    log.write(tree)
    log.write(f'total_time      : {total_time}')
    log.write(f'People / second : {tree.get_person_count() / total_time}')
    log.write('')


# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(start_id, tree):
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5

    print('\n\n\nWARNING: BFS (Limit of 5 threads) function not written')

    pass

# -----------------------------------------------------------------------------
# You must not change this function
# The goal is to limit the number of threads in part2 to 5
def part3(log, start_id, generations):
    tree = Tree(start_id)

    req = Request_thread(f'{TOP_API_URL}/start/{generations}')
    req.start()
    req.join()

    log.start_timer('Breadth-First')
    breadth_fs_pedigree_limit5(start_id, tree)
    total_time = log.stop_timer()

    req = Request_thread(f'{TOP_API_URL}/end')
    req.start()
    req.join()

    tree.display(log)
    log.write(tree)
    log.write(f'total_time      : {total_time}')
    log.write(f'People / second : {tree.get_person_count() / total_time}')
    log.write('')


# -----------------------------------------------------------------------------
def main():
    log = Log(show_terminal=True, filename_log='assignment.log')

    # starting family
    req = Request_thread(TOP_API_URL)
    req.start()
    req.join()

    print(f'Starting Family id: {req.response["start_family_id"]}')
    start_id = req.response['start_family_id']

    part1(log, start_id, 6)
    part2(log, start_id, 6)
    part3(log, start_id, 6)


if __name__ == '__main__':
    main()

