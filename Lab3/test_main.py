import unittest
from main import validate_interval, overlaps, find_conflicts, format_conflicts, sort_lessons

class ScheduleTests(unittest.TestCase):
    def setUp(self):
        self.a = {"day":"Понедельник","start":"09:00","end":"10:30","room":"301","subject":"Программирование"}
        self.b = {"day":"Понедельник","start":"10:00","end":"11:30","room":"301","subject":"Базы данных"}

    def test_validate(self):
        self.assertEqual(validate_interval(self.a)["room"], "301")

    def test_overlaps_true(self):
        self.assertTrue(overlaps(self.a, self.b))

    def test_different_days(self):
        self.assertFalse(overlaps(self.a, dict(self.b, day="Вторник")))

    def test_find_conflicts(self):
        self.assertEqual(len(find_conflicts([self.a, self.b])), 1)

    def test_different_rooms(self):
        self.assertEqual(find_conflicts([self.a, dict(self.b, room="205")]), [])

    def test_format(self):
        report = format_conflicts(find_conflicts([self.a, self.b]))
        self.assertIn("Обнаруженные пересечения", report)

    def test_bad_interval(self):
        with self.assertRaises(ValueError):
            validate_interval(dict(self.a, start="11:00", end="10:00"))

    def test_bad_time(self):
        with self.assertRaises(ValueError):
            validate_interval(dict(self.a, start="9 AM"))

    def test_sort_does_not_change_source(self):
        source = [self.b, self.a]
        sort_lessons(source)
        self.assertEqual(source[0]["subject"], "Базы данных")

if __name__ == "__main__":
    unittest.main()
