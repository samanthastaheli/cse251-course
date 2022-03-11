from concurrent.futures import thread
import threading
import time

x = 8192

lock = threading.Lock()

def double():
    global x #allows func to manipulate global var
    lock.aquire() #cannot lock same thing twice so will aquaire when lock is avalible
    while x < 16384:
        x *= 2
        print(x)
        time.sleep(1) #makes so not exeucte in millisecs so can see whats happening
    print('Reached the mamximum!')
    lock.release()

def halve():
    global x
    lock.acquire()
    while x > 1:
        x /= 2
        print(x)
        time.sleep(1)
    lock.release()
    
t1 = threading.Thread(target=halve)
t2 = threading.Thread(target=double)

t1.start()
t2.start()