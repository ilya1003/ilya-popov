"""Автоматические проверки основной части и варианта 3."""

import copy
import unittest

from university_rating.calculations import calculate_average, determine_status
from university_rating.rating import build_rating, build_group_ratings
from university_rating.validation import validate_scores


class RatingTests(unittest.TestCase):
    def test_empty_average(self):
        self.assertIsNone(calculate_average([]))

    def test_status_boundary(self):
        self.assertEqual(determine_status(49.99), 'не допущен')
        self.assertEqual(determine_status(50), 'допущен')

    def test_invalid_score(self):
        with self.assertRaises(ValueError):
            validate_scores([80, 101])

    def test_invalid_types(self):
        for value in ('80', True):
            with self.subTest(value=value), self.assertRaises(TypeError):
                validate_scores([value])

    def test_valid_boundary_scores(self):
        self.assertEqual(validate_scores([0, 100]), [0.0, 100.0])

    def test_missing_name(self):
        with self.assertRaisesRegex(ValueError, 'name'):
            build_rating([{'id': 1, 'group': 'A', 'scores': [70]}])

    def test_source_is_not_changed(self):
        students = [{'id': 1, 'name': 'Test', 'group': 'A', 'scores': [70, 80]}]
        before = copy.deepcopy(students)
        build_group_ratings(students)
        self.assertEqual(students, before)

    def test_empty_students(self):
        self.assertEqual(build_group_ratings([]), {})

    def test_group_ratings_are_separate_and_sorted(self):
        students = [
            {'id': 1, 'name': 'A', 'group': 'X', 'scores': [60]},
            {'id': 2, 'name': 'B', 'group': 'Y', 'scores': [90]},
            {'id': 3, 'name': 'C', 'group': 'X', 'scores': [80]},
        ]
        ratings = build_group_ratings(students)
        self.assertEqual([row['name'] for row in ratings['X']], ['C', 'A'])
        self.assertEqual([row['name'] for row in ratings['Y']], ['B'])

    def test_no_scores_last_in_own_group(self):
        students = [
            {'id': 1, 'name': 'NoScores', 'group': 'X', 'scores': []},
            {'id': 2, 'name': 'HasScores', 'group': 'X', 'scores': [0]},
        ]
        self.assertEqual([row['name'] for row in build_group_ratings(students)['X']], ['HasScores', 'NoScores'])

    def test_equal_average_stable_order(self):
        students = [
            {'id': 1, 'name': 'First', 'group': 'X', 'scores': [75]},
            {'id': 2, 'name': 'Second', 'group': 'X', 'scores': [75]},
        ]
        self.assertEqual([row['name'] for row in build_group_ratings(students)['X']], ['First', 'Second'])


if __name__ == '__main__':
    unittest.main()
