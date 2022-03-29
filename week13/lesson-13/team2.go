/* ---------------------------------------
Course: CSE 251
Lesson Week: ?12
File: team.go
Author: Brother Comeau
Purpose: team activity - finding primes
Instructions:
- Process the array of numbers, find the prime numbers using goroutines
worker()
This goroutine will take in a list/array/channel of numbers.  It will place
prime numbers on another channel
readValue()
This goroutine will display the contents of the channel containing
the prime numbers
--------------------------------------- */
package main

import (
	"fmt"
	"sync"
)

func isPrime(n int) bool {
	// Primality test using 6k+-1 optimization.
	// From: https://en.wikipedia.org/wiki/Primality_test

	if n <= 3 {
		return n > 1
	}

	if n%2 == 0 || n%3 == 0 {
		return false
	}

	i := 5
	for (i * i) <= n {
		if n%i == 0 || n%(i+2) == 0 {
			return false
		}
		i += 6
	}
	return true
}

func worker(id int, numbers chan int, primes chan int, wg *sync.WaitGroup) {
	for num := range numbers {
		//fmt.Println("worker", id, ", num=", num)
		if isPrime(num) {
			primes <- num
		}

		// subtract one from the semaphore
		wg.Done()
	}

}

func readValues(primes chan int) int {
	var total int = 0
	for range primes {
		//fmt.Println("prime =", val)
		total += 1
	}
	return total
}

func main() {

	workers := 100000
	numberValues := 100_000
	start := 10_000_000_000

	// create one channel to send/receive the numbers
	numbers := make(chan int, numberValues)

	// create another channel to send/receive the prime numbers
	primes := make(chan int, numberValues)

	// create a wait group as a barrier to wait until all goroutinues finish
	wg := new(sync.WaitGroup)

	// create workers
	for w := 1; w <= workers; w++ {
		go worker(w, numbers, primes, wg)
	}

	for i := start; i < start+numberValues; i++ {

		// add one to the wait group (semaphore)
		wg.Add(1)

		// send the number
		numbers <- i
	}

	// wait until all goroutines finish
	wg.Wait()

	// close the channels so we can process the results
	close(numbers)
	close(primes)

	// read off all the primes from the primes buffer
	total := readValues(primes)

	fmt.Println("Primes found= ", total)
}
