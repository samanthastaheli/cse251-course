from concurrent.futures import thread
import threading
from random import randrange

PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 5

total_meals = 0

SLEEP_REDUCTION_FACTOR = 10

class Philo(threading.Thread):
    def __init__(self, index,
                 left_fork: threading.Lock, 
                 right_fork: threading.Lock,
                 lock: threading.Lock) -> None:
        threading.Thread.__init__(self)
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.time_eating = 0
        self.time_thinking = 0
        self.lock = lock

    def run(self):
        global total_meals

        while(True):
            pass