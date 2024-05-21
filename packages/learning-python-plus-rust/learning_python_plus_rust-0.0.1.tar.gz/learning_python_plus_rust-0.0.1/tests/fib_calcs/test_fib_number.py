from unittest import main, TestCase
from learning_python_plus_rust.fib_calcs import fib_number


class TestFibNumber(TestCase):
    def test_negative(self):
        self.assertEqual(fib_number.recurring_fibonacci_number(n=-1), None)

    def test_zero(self):
        self.assertEqual(fib_number.recurring_fibonacci_number(n=0), 0)

    def test_one(self):
        self.assertEqual(fib_number.recurring_fibonacci_number(n=1), 1)

    def test_two(self):
        self.assertEqual(fib_number.recurring_fibonacci_number(n=2), 1)

    def test_twenty(self):
        self.assertEqual(fib_number.recurring_fibonacci_number(n=20), 6765)


if __name__ == "__main__":
    main()
