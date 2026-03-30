def fibonacci_sequence(n):
    fib_sequence = []
    a, b = 0, 1
    for _ in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence

first_20_fib_numbers = fibonacci_sequence(20)
print(first_20_fib_numbers)