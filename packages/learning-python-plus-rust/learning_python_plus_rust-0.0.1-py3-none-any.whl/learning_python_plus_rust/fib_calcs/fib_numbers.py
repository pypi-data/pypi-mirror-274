from .fib_number import recurring_fibonacci_number


def calculate_numbers(n: list[int]) -> list[int]:
    return [recurring_fibonacci_number(n=i) for i in n]
