import time
from threading import Condition, Thread
import random

items = []
condition = Condition()


class consumer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def consume(self):
        pass

    def run(self):
        pass


class producer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def produce(self):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    producer = producer()
    consumer = consumer()
    
    producer.start()
    consumer.start()
    
    producer.join()
    producer.join()
