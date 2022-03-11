#include <iostream>
#include <cstdlib>
#include <pthread.h>

using namespace std;

#define NUM_THREADS 5

void *PrintHello(void *threadid) {
   long tid;
   tid = (long)threadid;
   cout << "Hello World! Thread ID, " << tid << "\n";
   pthread_exit(NULL);

   return NULL;
}

int main () {
   pthread_t threads[NUM_THREADS];

   for(int i = 0; i < NUM_THREADS; i++ ) {
      cout << "\n main() : creating thread, " << i << endl;
      int rc = pthread_create(&threads[i], NULL, PrintHello, (void *)i);

      if (rc) {
         cout << "Error:unable to create thread," << rc << endl;
         exit(-1);
      }
   }
   pthread_exit(NULL);
}
