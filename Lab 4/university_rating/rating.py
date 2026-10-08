"""Построение общего рейтинга и рейтингов учебных групп."""

from .calculations import calculate_average, determine_status
from .validation import validate_scores, validate_student


def build_student_result(student):
    """Создать итоговую запись без изменения исходной."""
    validate_student(student)
    scores = validate_scores(student['scores'])
    average = calculate_average(scores)
    return {
        'id': student['id'],
        'name': student['name'],
        'group': student['group'],
        'average': average,
        'status': determine_status(average),
    }


def _sort_key(item):
    average = item['average']
    return average is not None, average if average is not None else 0


def build_rating(students):
    """Отсортировать студентов по среднему, сохранив исходные данные."""
    if not isinstance(students, (list, tuple)):
        raise TypeError('students должен быть списком или кортежем')
    results = [build_student_result(item) for item in students]
    return sorted(results, key=_sort_key, reverse=True)


def build_group_ratings(students):
    """Вернуть словарь {группа: рейтинг} для каждой учебной группы."""
    grouped = {}
    for row in build_rating(students):
        grouped.setdefault(row['group'], []).append(row)
    return grouped
