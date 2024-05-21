import argparse
from learning_python_plus_rust.fib_calcs.fib_number import recurring_fibonacci_number


def fib_numb() -> None:
    parser = argparse.ArgumentParser(description="Calculate Fibonacci numbers")
    parser.add_argument(
        "n",
        type=int,
        help="The Fibonacci number to calculate",
    )
    args = parser.parse_args()
    print(f"Your Fibonacci number is: {recurring_fibonacci_number(args.n)}")
