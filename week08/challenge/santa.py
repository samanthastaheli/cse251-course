import threading
import string

'''
recursion example
function calls self over and over divides list in half until 1 item in list
'''

def deliver_presents_recursively(houses):
    # base case, O(1)?
    if len(houses) == 1:
        house = houses[0]
        print(f'Delivering presents to {house}')
    else:
        # divide list in 2
        mid = len(houses) // 2 # dbl backslash means integer divison, single makes float
        first_half = houses[0:mid] # everything after mid value
        second_half = houses[mid:len(houses)] # everything before mid value

        print(f'{first_half=}') # prints 'value name = value'
        print(f'{second_half=}')

        deliver_presents_recursively(first_half)
        deliver_presents_recursively(second_half)


if __name__ == '__main__':
    houses = list(string.ascii_lowercase + string.ascii_uppercase)
    deliver_presents_recursively(houses)
