'''
- figure out base case
- else do somthing else
- helpful to store itermediate steps into variables
    - reasons:
        - documentationss
        - debugging reference
'''
# print numbers recursively (don't print with brackets)
def print_numbers(numbers):
    if len(numbers) == 1:
        number = numbers[0]
        print(f'the number you were looking for... {number}')
    else:
        mid = len(numbers) // 2
        first_half = numbers[:mid]
        second_half = numbers[mid:]

        print(f'{first_half=}')
        print(f'{second_half=}')

        print_numbers(first_half)
        print_numbers(second_half)

if __name__ == '__main__':
    numbers = list(i for i in range(101))
    print_numbers(numbers)
