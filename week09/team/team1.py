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

def philoLoop(forkSemaphore, forks, philosophers, index):
  # recursion, function calls itself 
  while(True):
    toggleLeftFork(forkSemaphore, forks, index)
    toggleRightFork(forkSemaphore, forks, index)
    if philosophers[index] == MAX_MEALS:
      toggleLeftFork(forkSemaphore, forks, index)
      toggleRightFork(forkSemaphore, forks, index)
      del philosophers[index]
      del forks[index]
      print(f'Philosophers {index} has reached maximum meals.')
    elif (leftForkAcquired and rightForkAcquired):
      pass

def grabLeftFork(forkSemaphore, forks, index):
  forkSemaphore.acquire()
  if (forks[index]==0):
    forks[index] = 1
    return True
  else:
    forkSemaphore.release()
    return False

def grabRightFork(forkSemaphore, forks, index):
  forkSemaphore.acquire()
  if (index == (PHILOSOPHERS - 1)):
    if (forks[0] == 0):
      forks[0] = 1
      return True
    else:
      forkSemaphore.release()
      return False
  else:
    if (forks[index+1]==1):
      forks[index] = 1
      return True
    else:
      forkSemaphore.release()
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
  
def feedPhilosopher( cv, forks, forkSemaphore,  ):
  forkSemaphore.acquire()
  forkSemaphore.acquire()

def main():
  # TODO - create the forks
  forks = []
  philosophers = []
  for i in range(0, PHILOSOPHERS):
    forks.append(0) #append 0 because 0 means fork is not being used
    philosophers.append(0) #start with 0 because have had 0 meals
  
  condition = threading.Condition()
  forkSemaphore = threading.Semaphore(5)

  for i in range(PHILOSOPHERS):
    t = threading.Thread(target=philoLoop, args=(forkSemaphore, forks, philosophers, i))
    t.start()
    t.join()

  # TODO - Start them eating and thinking

  # TODO - Display how many times each philosopher ate

  pass



if __name__ == '__main__':
    main()