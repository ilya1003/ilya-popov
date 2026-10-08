import unittest

from main import (
    Student,
    CsvParser,
    JsonParser,
    MemoryParser,
    ImportService,
)


class ImportServiceTests(unittest.TestCase):

    def test_student_creation(self):
        student = Student(1, "Илья", "ИС-23")
        self.assertEqual(student.student_id, 1)
        self.assertEqual(student.name, "Илья")
        self.assertEqual(student.group, "ИС-23")

    def test_csv_parser(self):
        data = """id,name,group
1,Илья,ИС-23
2,Алина,ИС-24
"""
        result = ImportService(CsvParser()).import_students(data)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "Илья")
        self.assertEqual(result[1].group, "ИС-24")

    def test_json_parser(self):
        data = """
[
    {"id": 1, "name": "Илья", "group": "ИС-23"}
]
"""
        result = ImportService(JsonParser()).import_students(data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], Student(1, "Илья", "ИС-23"))

    def test_memory_parser(self):
        students = [
            Student(1, "Илья", "ИС-23"),
            Student(2, "Алина", "ИС-24"),
        ]

        result = ImportService(MemoryParser(students)).import_students("")

        self.assertEqual(result, students)

    def test_invalid_student_id(self):
        with self.assertRaises(ValueError):
            Student(0, "Илья", "ИС-23")

    def test_empty_student_name(self):
        with self.assertRaises(ValueError):
            Student(1, "", "ИС-23")

    def test_invalid_json(self):
        with self.assertRaises(ValueError):
            ImportService(JsonParser()).import_students('{"id": 1}')

    def test_parser_replacement(self):
        csv_data = "id,name,group\n1,Илья,ИС-23\n"
        json_data = '[{"id": 2, "name": "Алина", "group": "ИС-24"}]'

        csv_result = ImportService(CsvParser()).import_students(csv_data)
        json_result = ImportService(JsonParser()).import_students(json_data)

        self.assertEqual(csv_result[0].name, "Илья")
        self.assertEqual(json_result[0].name, "Алина")


if __name__ == "__main__":
    unittest.main(verbosity=2)
