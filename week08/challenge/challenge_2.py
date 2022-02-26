
# TODO write a recursive function that takes a number and
# returns the sum of all the numbers from one to that number
def cumulative(number):
    
    # print out the current return value from a recursive call
    # plus the current number and the sum (total).
    # Should look like this:
    # 1 + 2 = 3
    # 3 + 3 = 6
    # 6 + 4 = 10
    # 10 + 5 = 15
    # 15 + 6 = 21
    # 21 + 7 = 28
    # 28 + 8 = 36
    # 36 + 9 = 45
    # 45 + 10 = 55
    #print(f'{value} + {number} = {total}')
    
    pass #delete this line

if __name__ == '__main__':
    value = cumulative(10)
    print(f'return value = {value}')
    assert(value == 55)
