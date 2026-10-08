"""Автоматические тесты лабораторной № 5, вариант 14."""
import unittest
from main import Payment, StudentAccount


class AccountTests(unittest.TestCase):
    def setUp(self):
        self.account = StudentAccount(1, 'Amina')

    def test_charge(self):
        self.account.charge(1500)
        self.assertEqual(self.account.balance, 1500)

    def test_payment(self):
        self.account.charge(1000)
        self.account.pay(300)
        self.assertEqual(self.account.balance, 700)

    def test_full_payment(self):
        self.account.charge(1000)
        self.account.pay(1000)
        self.assertEqual(self.account.balance, 0)

    def test_overpayment_does_not_change_state(self):
        self.account.charge(100)
        with self.assertRaises(ValueError):
            self.account.pay(101)
        self.assertEqual(self.account.balance, 100)
        self.assertEqual(len(self.account.history), 1)

    def test_zero_or_negative_amount(self):
        for amount in (0, -1):
            with self.assertRaises(ValueError):
                self.account.charge(amount)

    def test_invalid_type(self):
        for amount in (True, '100', None):
            with self.assertRaises(TypeError):
                self.account.pay(amount)

    def test_invalid_student(self):
        with self.assertRaises(ValueError):
            StudentAccount(0, 'Amina')
        with self.assertRaises(ValueError):
            StudentAccount(1, '  ')

    def test_history_is_immutable(self):
        self.account.charge(100)
        history = self.account.history
        self.assertIsInstance(history, tuple)
        self.assertIsInstance(history[0], Payment)
        with self.assertRaises(AttributeError):
            history[0].amount_tiyin = 0

    def test_fractional_amounts(self):
        self.account.charge(10.25)
        self.account.pay(0.10)
        self.assertEqual(self.account.balance, 10.15)

    def test_invalid_fraction(self):
        with self.assertRaises(ValueError):
            self.account.charge(10.001)


if __name__ == '__main__':
    unittest.main()
