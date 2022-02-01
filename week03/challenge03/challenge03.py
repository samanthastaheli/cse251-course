import multiprocessing as mp


def reverse_word(word):
    #TODO create a function that takes a list of 
    #     numbers and returns the list in reverse order
    #     don't use the built-in reverse function :)
    reverse_list = []
    letter_list = list(word)
    i = -1
    for i in range(len(letter_list)):
        letter = letter_list[i]
        reverse_list.append(letter)
        i-=1
    print(reverse_list) 

if __name__ == '__main__':
    
    # list of lists
    words = ["onomatopoeia", "first", "hello", "Pneumonoultramicroscopicsilicovolcanoconiosis", "zebra", "exit"]
    
    #TODO using 4 processes, reverse each word and print them out
    i = 1
    for i in range(len(words)):
        p = mp.Process(target=reverse_word, args=(words[i]))
        p.start()
        p.join()
        i+=1
    
    #Things to remember:
    # 1. Strings are immutable, so you need to treat them as lists of characters
    #   -see https://stackoverflow.com/questions/1228299/changing-one-character-in-a-string

    # 2. Range can be used with a start, end, and step (and the end value is not included)
    #    -see https://www.geeksforgeeks.org/python-range-function/
    
    # 3. Remember that the first index value in a list is 0