"""Точка входа лабораторной работы № 4, вариант 3."""

from .rating import build_group_ratings
from .report import format_group_ratings


def load_demo_data():
    """Вернуть примеры студентов двух учебных групп."""
    return [
        {'id': 101, 'name': 'Amina', 'group': 'IS-21', 'scores': [88, 92, 79]},
        {'id': 102, 'name': 'Dias', 'group': 'IS-21', 'scores': [45, 52, 48]},
        {'id': 103, 'name': 'Mira', 'group': 'IS-21', 'scores': []},
        {'id': 104, 'name': 'Ali', 'group': 'IS-22', 'scores': [90, 80, 85]},
        {'id': 105, 'name': 'Dana', 'group': 'IS-22', 'scores': [50, 50]},
        {'id': 106, 'name': 'Timur', 'group': 'IS-22', 'scores': []},
    ]


def main():
    """Показать рейтинг отдельно по каждой группе."""
    students = load_demo_data()
    ratings = build_group_ratings(students)
    print(format_group_ratings(ratings))


if __name__ == '__main__':
    main()
