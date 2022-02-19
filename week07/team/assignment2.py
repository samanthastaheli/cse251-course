from datetime import datetime, timedelta
from glob import glob
from unittest import result
from urllib import response
import requests
import json
import threading
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

# Const Values
TOP_API_URL = 'https://swapi.dev/api'

# Global Variables
call_count = 0
char_results = []
planets_results = []
starship_results = []
vehicles_results = []
species_results = []

# -------------------------------------------------------------------------------

def get_json(url):
    global call_count
    call_count += 1

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

    return data

def get_data(url):
    data = []
    for item in url:
        response = requests.get(item)
        json_data = response.json()
        data.append(json_data)

    return data

def callback_char(data):
    global char_results
    char_results = data

def callback_planets(data):
    global planets_results
    planets_results = data

def callback_starships(data):
    global starship_results
    starship_results = data

def callback_vehicles(data):
    global vehicles_results
    vehicles_results = data

def callback_species(data):
    global species_results
    species_results = data

def print_film_details(log, film_json):

    def display_names(title, name_list):
        log.write('')
        log.write(f'{title}: {len(name_list)}')
        names = sorted([item["name"] for item in name_list])
        log.write(str(names)[1:-1].replace("'", ""))


    log.write('-' * 40)
    log.write(f'Title   : {film_json["title"]}')
    log.write(f'Director: {film_json["director"]}')
    log.write(f'Producer: {film_json["producer"]}')
    log.write(f'Released: {film_json["release_date"]}')

    display_names('Characters', char_results)
    display_names('Planets', planets_results)
    display_names('Starships', starship_results)
    display_names('Vehicles', vehicles_results)
    display_names('Species', species_results)



def main():
    log = Log(show_terminal=True)

    log.start_timer('Starting to retrieve data from swapi.dev')

    # Retrieve Top API urls
    top_json = get_json(TOP_API_URL)
    film_url = top_json['films']
    film_json = get_json(f'{film_url}6')

    # CREATING OUR POOLS FOR THE 5 DIFFERENT DATA SETS
    pool = mp.Pool(5)

    pool.apply_async(get_data, args = (film_json['characters'], ), callback = callback_char)

    pool.apply_async(get_data, args = (film_json['planets'], ), callback = callback_planets)

    pool.apply_async(get_data, args = (film_json['starships'], ), callback = callback_starships)

    pool.apply_async(get_data, args = (film_json['vehicles'], ), callback = callback_vehicles)

    pool.apply_async(get_data, args = (film_json['species'], ), callback = callback_species)

    # Close all pools and join
    pool.close()
    pool.join()

    # log.write(urls)

    # Retrieve film 6 details   

    # Display results
    print_film_details(log, film_json)

    log.write('')
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to swapi server')


if __name__ == "__main__":
    main()