import threading

def display_hello():
    print ("Hello, World!")

print('Before the thread')
thread = threading.Timer(3.0, display_hello)
thread.start()
print('After the thread - End of program')