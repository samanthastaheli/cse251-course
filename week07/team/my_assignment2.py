from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

# Const Values
TOP_API_URL = r'https://swapi.dev/api'

# Global Variables
call_count = 0

def update_count():
    global call_count
    call_count += 1

# TODO Add your threaded class definition here
class use_thread(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.data = response.json()
            update_count()
        pass


# TODO Add any functions you need here
def create_thread_list(thread, target):
    return [use_thread(i) for i in (thread.data['results'][5][target])]

def get_data(thread_list):
    new_list = []
    for i in range(len(thread_list)):
        thread_list[i].start()
        thread_list[i].join()
        new_list.append(thread_list[i].data['name'])
    return sorted(new_list)

# def get_planets(planets_thread):
#     listofPlanets = []
#     for i in range(len(planets_thread)):
#         planets_thread[i].start()
#         planets_thread[i].join()
#         listofPlanets.append(planets_thread[i].data['name'])
#     return sorted(listofPlanets)

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from swapi.dev')

    # TODO Retrieve Top API urls
    # TODO Retireve Details on film 6    
    # TODO Display results
    thread1 = use_thread(TOP_API_URL)
    thread1.start()
    thread1.join()
    thread1.url = thread1.data['films']
    thread2 = use_thread(thread1.url)
    thread2.start()
    thread2.join()
    print("Title   :   ", thread2.data['results'][5]['title'])
    print("Director   : ", thread2.data['results'][5]['director'])
    print("Producer   : ", thread2.data['results'][5]['producer'])
    print("Released   : ", thread2.data['results'][5]['release_date'])
    print("Characters  : ", len(thread2.data['results'][5]['characters']))

    listOfThreadsCharacters = create_thread_list(thread2, 'characters')
    listOfThreadsPlanets = create_thread_list(thread2, 'planets')
    listOfThreadsStarships = create_thread_list(thread2, 'starships')
    listOfThreadsVehicles = create_thread_list(thread2, 'vehicles')
    listOfThreadsSpecies = create_thread_list(thread2, 'species')

    listofPlanets = get_data(listOfThreadsPlanets)
    listofCharacters = get_data(listOfThreadsCharacters)
    listOfStarships = get_data(listOfThreadsStarships)
    listOfVehicles = get_data(listOfThreadsVehicles)
    listOfSpecies = get_data(listOfThreadsSpecies)

    print(', '.join(listofCharacters))
    print()

    print("Planets  : ", len(thread2.data['results'][5]['planets']))
    print(', '.join(listofPlanets))
    print()

    print("Starships  : ", len(thread2.data['results'][5]['starships']))
    print(', '.join(listOfStarships))
    print()

    print("Vehicles  : ", len(thread2.data['results'][5]['vehicles']))
    print(', '.join(listOfVehicles))
    print()

    print("Species  : ", len(thread2.data['results'][5]['species']))
    print(', '.join(listOfSpecies))
    print()

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to swapi server')
    

if __name__ == "__main__":
    main()
