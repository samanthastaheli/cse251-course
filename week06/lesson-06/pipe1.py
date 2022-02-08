import multiprocessing

END_MESSAGE = 'Goodbye!!'


def sender(conn: multiprocessing.Pipe, msgs):
    """ 
    function to send messages to other end of pipe 
    """
    for msg in msgs:
        # TODO send a message
        
        print(f"Sent the message: {msg}")
        
    # TODO send the end message and close the connection


def receiver(conn: multiprocessing.Pipe):
    """ 
    function to print the messages received from other end of pipe 
    """
    while True:
        
        #TODO reveive the message
        msg = ""
        
        if msg == END_MESSAGE:
            break
        print(f"Received the message: {msg}")
        
    # TODO don't forget to close the connection


if __name__ == "__main__":

    # messages to be sent
    msgs = ["hello", "hey", "You?", "hi"]

    # TODO create a pipe

    # create two new processes: one to send msgs and one to receive it
    p1 = multiprocessing.Process()
    p2 = multiprocessing.Process()

    # running processes
    p1.start()
    p2.start()

    # wait until processes finish
    p1.join()
    p2.join()
