"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls

Instructions:

- Review instructions in I-Learn.

"""

# from ast import Return
# from datetime import datetime, timedelta
# import threading
# from urllib import request 
# import requests
# import json

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    if request.status_code == 200:
        data = json.load(request)
        print('Drawing Card')
        print(data)
            # self.remaining += -1

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52
        self.shuffle = requests.get(r"http://deckofcardsapi.com/api/deck/zyfer350mvmd/shuffle/")
        

    def reshuffle(self):
        # TODO - add call to reshuffle
        # result =  requests.get(f"http://deckofcardsapi.com/api/deck/{self.id}/shuffle/")
        # if request.status_code == 200:
        #     data = json.load()
        #     print("Shuffling")
        #     print(data)
        pass

    def draw_card(self):
        # TODO add call to get a card
        # print("Drawing card")
        url = requests.get(r"http://deckofcardsapi.com/api/deck/zyfer350mvmd/draw/?count=1")
        thread = Request_thread(url)
       
        card = data['cards']
        return card['value']


    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'zyfer350mvmd'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(i, card, flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<

