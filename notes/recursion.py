def factorial(n):
    print(f'computing... {n}')
    if n == 1:
        return 1
    else:
        return n*factorial(n-1)

print(f'result... {factorial(4)}')