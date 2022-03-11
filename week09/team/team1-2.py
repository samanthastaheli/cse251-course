"""
Course: CSE 251
Lesson Week: 09
File: team1.py

Purpose: team activity - Dining philosophers problem

Problem statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks
are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can
only eat spaghetti when they have both left and right forks. Each fork can be
held by only one philosopher and so a philosopher can use the fork only if it
is not being used by another philosopher. After an individual philosopher
finishes eating, they need to put down both forks so that the forks become
available to others. A philosopher can only take the fork on their right or
the one on their left as they become available and they cannot start eating
before getting both forks.  When a philosopher is finished eating, they think 
for a little while.

Eating is not limited by the remaining amounts of spaghetti or stomach space;
an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm)
such that no philosopher will starve

Instructions:

        **************************************************
        ** DO NOT search for a solution on the Internet **
        ** your goal is not to copy a solution, but to  **
        ** work out this problem.                       **
        **************************************************

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout.
- philosophers need to eat for 3 to 5 seconds when they get both forks.  
    - time.sleep()
    - lock.wait()
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers.
- Use threads for this problem.
- When you get your program working, how to you prove that no philosopher will starve?
  (Just looking at output from print() statements is not enough)
- Are the philosophers each eating and thinking the same amount?
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat


"""
import time
import threading


PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 5

def eating(forks, philos, index):
    left_fork = forks[index - 1]
    right_fork = forks[index]
    

def grabFork(forks, philos, index):
    if (index == (PHILOSOPHERS - 1)):
        if (forks[0] == 0):
            forks[0] = 1
            return True
    elif (forks[index]==0):
        forks[index] = 1
        return True
    else:
        return False

def eatPasta():
    pass

def canEat(forks, index):
    left_fork = forks[index]
    right_fork = forks[index + 1]
    if left_fork == 0 and right_fork == 0:
        forks[index] = 1
        forks[index + 1] = 1
        return True
    elif left_fork == 1 or right_fork == 1:
        return False
  

def main():
    # create the forks
    forks = [1, 2, 3, 4, 5]
    philos = [0, 0, 0, 0, 0] # start with 0 because have had 0 meals

    condition = threading.Condition()

    philo1 = threading.Thread(target=eating, args=(condition, forks, philos, 1))
    philo2 = threading.Thread(target=eating, args=(condition, forks, philos, 2))
    philo3 = threading.Thread(target=eating, args=(condition, forks, philos, 3))
    philo4 = threading.Thread(target=eating, args=(condition, forks, philos, 4))
    philo5 = threading.Thread(target=eating, args=(condition, forks, philos, 5))

    # Start them eating and thinking
    philo1.start()
    philo2.start()
    philo3.start()
    philo4.start()
    philo5.start()
    
    philo1.join()
    philo2.join()
    philo3.join()
    philo4.join()
    philo5.join()

    # TODO - Display how many times each philosopher ate
    print()


if __name__ == '__main__':
    main()