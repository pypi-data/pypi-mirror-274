from typing import Optional


def recurring_fibonacci_number(n: int) -> Optional[int]:
    if n < 0:
        return None
    if n <= 1:
        return n

    return recurring_fibonacci_number(n - 1) + recurring_fibonacci_number(n - 2)
