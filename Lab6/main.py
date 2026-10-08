from typing import Protocol
import csv
import json
from io import StringIO


class Student:
    """Модель студента."""

    def __init__(self, student_id: int, name: str, group: str):
        if isinstance(student_id, bool) or not isinstance(student_id, int):
            raise TypeError("ID должен быть целым числом")
        if student_id <= 0:
            raise ValueError("ID должен быть положительным")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя не может быть пустым")
        if not isinstance(group, str) or not group.strip():
            raise ValueError("Группа не может быть пустой")

        self.student_id = student_id
        self.name = name.strip()
        self.group = group.strip()

    def __repr__(self):
        return (
            f"Student(id={self.student_id}, "
            f"name='{self.name}', group='{self.group}')"
        )

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return (
            self.student_id == other.student_id
            and self.name == other.name
            and self.group == other.group
        )


class StudentParser(Protocol):
    """Общий контракт парсера студентов."""

    def parse(self, data: str) -> list[Student]:
        ...


class CsvParser:
    """Импорт студентов из CSV."""

    def parse(self, data: str) -> list[Student]:
        students = []
        reader = csv.DictReader(StringIO(data))

        for row in reader:
            students.append(
                Student(
                    int(row["id"]),
                    row["name"],
                    row["group"],
                )
            )
        return students


class JsonParser:
    """Импорт студентов из JSON."""

    def parse(self, data: str) -> list[Student]:
        items = json.loads(data)

        if not isinstance(items, list):
            raise ValueError("JSON должен содержать список студентов")

        students = []
        for item in items:
            if not isinstance(item, dict):
                raise ValueError("Элемент JSON должен быть объектом")

            students.append(
                Student(
                    int(item["id"]),
                    item["name"],
                    item["group"],
                )
            )
        return students


class MemoryParser:
    """Тестовый парсер, возвращающий студентов из памяти."""

    def __init__(self, students: list[Student] | None = None):
        self.students = students or []

    def parse(self, data: str) -> list[Student]:
        return self.students.copy()


class ImportService:
    """Сервис импорта, работающий с любым StudentParser."""

    def __init__(self, parser: StudentParser):
        self._parser = parser

    def import_students(self, data: str) -> list[Student]:
        return self._parser.parse(data)


def print_students(title: str, students: list[Student]) -> None:
    print(f"\n{title}")
    for student in students:
        print(
            f"ID: {student.student_id}, "
            f"Имя: {student.name}, "
            f"Группа: {student.group}"
        )


if __name__ == "__main__":
    csv_data = """id,name,group
1,Илья,ИС-23
2,Алина,ИС-24
3,Данияр,ИС-23
"""

    json_data = """
[
    {"id": 4, "name": "Алексей", "group": "ИС-25"},
    {"id": 5, "name": "Мария", "group": "ИС-24"}
]
"""

    memory_students = [
        Student(6, "Арман", "ИС-23"),
        Student(7, "Диана", "ИС-24"),
    ]

    csv_service = ImportService(CsvParser())
    json_service = ImportService(JsonParser())
    memory_service = ImportService(MemoryParser(memory_students))

    print_students("Импорт из CSV:", csv_service.import_students(csv_data))
    print_students("Импорт из JSON:", json_service.import_students(json_data))
    print_students("Импорт из памяти:", memory_service.import_students(""))
