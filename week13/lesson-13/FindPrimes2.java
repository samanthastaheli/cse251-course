import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

class FindPrimeThread2 extends Thread {
    List<Long> numbers;
    List<Long> primes = Collections.synchronizedList(new ArrayList<Long>());

    public FindPrimeThread2(List<Long> numbers, List<Long> primes) {
        this.numbers = numbers;
        this.primes = primes;
    }

    private static boolean isPrime(long n) {
        // Corner cases
        if (n <= 1)
            return false;
        if (n <= 3)
            return true;

        // This is checked so that we can skip
        // middle five numbers in below loop
        if (n % 2 == 0 || n % 3 == 0)
            return false;

        for (long i = 5; i * i <= n; i = i + 6)
            if (n % i == 0 || n % (i + 2) == 0)
                return false;

        return true;
    }

    @Override
    public void run() {
        //System.out.println("Thread " + Thread.currentThread().getId() + " is running, checking from " + numbers.get(0)
        //        + " to " + numbers.get(numbers.size() - 1));
        for (long number : numbers) {
            if (isPrime(number)) {
                //System.out.println("prime: " + number);
                primes.add(number);
            }
        }
    }

}

class FindPrimes2 {

    static int MAX_THREADS = 100;

    public static void main(String[] args) {

        long start = 10_000_000_000l;
        int count = 100_000;
        // long start = 100l;
        // int count = 100;

        List<Long> numbers = new ArrayList<>();
        for (long i = start; i < start + count; i++) {
            numbers.add(i);
        }

        // create a thread safe list to store the prime numbers found
        List<Long> primes = Collections.synchronizedList(new ArrayList<>());

        // list of our threads
        ArrayList<FindPrimeThread2> threads = new ArrayList<>();

        // how big each sub-array should be for each thread to search over
        int partitionSize = count / MAX_THREADS;

        for (int i = 0; i < count; i += partitionSize) {

            int end = i + partitionSize;

            // System.out.println(String.format("start=%s, end=%s", i, end));
            List<Long> subList = numbers.subList(i, end);

            FindPrimeThread2 thread = new FindPrimeThread2(subList, primes);
            thread.start();
            threads.add(thread);
        }

        for (FindPrimeThread2 thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        System.out.println("total primes = " + primes.size());
    }
}