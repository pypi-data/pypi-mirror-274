from unittest import main, TestCase
from unittest.mock import patch
from learning_python_plus_rust.fib_calcs import fib_numbers


class TestFibNumbers(TestCase):
    @patch("learning_python_plus_rust.fib_calcs.fib_numbers.recurring_fibonacci_number")
    def test_calculate_numbers(self, mock_fib_calc):
        expected_outcome = [mock_fib_calc.return_value, mock_fib_calc.return_value]
        self.assertEqual(fib_numbers.calculate_numbers(n=[3, 4]), expected_outcome)
        self.assertEqual(2, len(mock_fib_calc.call_args_list))
        self.assertEqual({"n": 3}, mock_fib_calc.call_args_list[0][1])
        self.assertEqual({"n": 4}, mock_fib_calc.call_args_list[1][1])

    def test_functional(self):
        self.assertEqual([2, 3, 5], fib_numbers.calculate_numbers(n=[3, 4, 5]))


if __name__ == "__main__":
    main()
