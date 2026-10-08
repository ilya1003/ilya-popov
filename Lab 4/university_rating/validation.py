"""Проверка данных студентов и оценок."""


def validate_scores(scores):
    """Вернуть проверенную копию оценок от 0 до 100."""
    if not isinstance(scores, (list, tuple)):
        raise TypeError('scores должен быть списком или кортежем')
    checked = []
    for score in scores:
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError('Балл должен быть числом')
        if not 0 <= score <= 100:
            raise ValueError('Балл должен быть от 0 до 100')
        checked.append(float(score))
    return checked


def validate_student(student):
    """Проверить обязательные поля и учебную группу студента."""
    if not isinstance(student, dict):
        raise TypeError('Запись студента должна быть словарём')
    missing = {'id', 'name', 'scores', 'group'} - student.keys()
    if missing:
        raise ValueError(f'Отсутствуют поля: {sorted(missing)}')
    if not isinstance(student['name'], str) or not student['name'].strip():
        raise ValueError('name должен быть непустой строкой')
    if not isinstance(student['group'], str) or not student['group'].strip():
        raise ValueError('group должен быть непустой строкой')
