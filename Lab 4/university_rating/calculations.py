"""Предметные вычисления рейтинга."""

PASSING_AVERAGE = 50


def calculate_average(scores):
    """Вычислить среднее или None при отсутствии оценок."""
    return sum(scores) / len(scores) if scores else None


def determine_status(average):
    """Определить допуск по среднему баллу."""
    if average is None:
        return 'нет данных'
    return 'допущен' if average >= PASSING_AVERAGE else 'не допущен'
