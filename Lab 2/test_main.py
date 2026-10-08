"""Проверки лабораторной работы №2 (запуск: python -m unittest -v)."""
import unittest
from main import task1, task2, task3, task4, task5, taxi_fare, comparison


class Lab2Tests(unittest.TestCase):
    def test_state(self):
        self.assertEqual(task1(), 11)

    def test_purchase(self):
        self.assertEqual(task2(2500, 4, 10), (10000, 1000, 9000))

    def test_grades(self):
        self.assertEqual([task3(x) for x in (95, 82, 60, 20)], ['A', 'B', 'C', 'F'])
        self.assertTrue(task3(101).startswith('Ошибка'))

    def test_accumulator(self):
        self.assertEqual(task4(), (40, 55, 4, 3, 1))

    def test_maximum(self):
        self.assertEqual(task5(), 91)

    def test_taxi(self):
        self.assertEqual(taxi_fare(10), (1700, 0, 1700))
        self.assertEqual(taxi_fare(20), (2900, 0, 2900))
        self.assertEqual(taxi_fare(25), (3500, 175, 3325))

    def test_negative_distance(self):
        with self.assertRaises(ValueError):
            taxi_fare(-1)

    def test_comparison(self):
        self.assertEqual(comparison(), (22, 22))


if __name__ == '__main__':
    unittest.main()
