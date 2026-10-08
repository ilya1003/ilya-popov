"""Текстовое представление рейтинга без печати."""


def format_average(value):
    """Представить средний балл с двумя знаками или прочерком."""
    return '—' if value is None else f'{value:.2f}'


def format_rating(rows):
    """Сформировать текст общего рейтинга."""
    lines = ['Рейтинг группы']
    for position, row in enumerate(rows, 1):
        lines.append(f"{position}. {row['name']}: {format_average(row['average'])} — {row['status']}")
    return '\n'.join(lines)


def format_group_ratings(group_ratings):
    """Сформировать отдельные таблицы рейтинга для учебных групп."""
    sections = []
    for group in sorted(group_ratings):
        lines = [f'Учебная группа: {group}']
        for position, row in enumerate(group_ratings[group], 1):
            lines.append(f"{position}. {row['name']}: {format_average(row['average'])} — {row['status']}")
        sections.append('\n'.join(lines))
    return '\n\n'.join(sections) if sections else 'Нет студентов'
