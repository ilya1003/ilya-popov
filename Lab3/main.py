from datetime import datetime

def _to_minutes(value):
    if not isinstance(value, str):
        raise TypeError("Время должно быть строкой")
    try:
        t = datetime.strptime(value, "%H:%M")
    except ValueError as exc:
        raise ValueError("Время должно иметь формат HH:MM") from exc
    return t.hour * 60 + t.minute

def validate_interval(lesson):
    """Проверяет корректность одного занятия."""
    if not isinstance(lesson, dict):
        raise TypeError("Занятие должно быть словарём")
    required = {"day", "start", "end", "room"}
    if not required.issubset(lesson):
        raise ValueError("Отсутствуют обязательные поля")
    if not isinstance(lesson["day"], str) or not lesson["day"].strip():
        raise ValueError("День не может быть пустым")
    if not isinstance(lesson["room"], str) or not lesson["room"].strip():
        raise ValueError("Аудитория не может быть пустой")
    start = _to_minutes(lesson["start"])
    end = _to_minutes(lesson["end"])
    if end <= start:
        raise ValueError("Время окончания должно быть позже начала")
    return dict(lesson)

def overlaps(first, second, break_minutes=0):
    """Проверяет пересечение двух занятий."""
    first = validate_interval(first)
    second = validate_interval(second)
    if first["day"] != second["day"]:
        return False
    a, b = _to_minutes(first["start"]), _to_minutes(first["end"]) + break_minutes
    c, d = _to_minutes(second["start"]), _to_minutes(second["end"]) + break_minutes
    return a < d and c < b

def find_conflicts(lessons, break_minutes=0):
    """Находит пересечения занятий в одной аудитории."""
    checked = [validate_interval(x) for x in lessons]
    result = []
    for i, first in enumerate(checked):
        for second in checked[i + 1:]:
            if first["room"] == second["room"] and overlaps(first, second, break_minutes):
                result.append((first, second))
    return result

def format_conflicts(conflicts):
    """Формирует текстовый отчёт."""
    if not conflicts:
        return "Конфликтов не обнаружено."
    lines = ["Обнаруженные пересечения:"]
    for n, (a, b) in enumerate(conflicts, 1):
        lines.append(
            f"{n}. {a['day']}: {a.get('subject', 'Занятие')} "
            f"({a['start']}-{a['end']}, ауд. {a['room']}) пересекается с "
            f"{b.get('subject', 'Занятие')} "
            f"({b['start']}-{b['end']}, ауд. {b['room']})."
        )
    return "\n".join(lines)

def sort_lessons(lessons):
    """Сортирует расписание, не изменяя исходный список."""
    checked = [validate_interval(x) for x in lessons]
    order = {"Понедельник": 1, "Вторник": 2, "Среда": 3,
             "Четверг": 4, "Пятница": 5, "Суббота": 6, "Воскресенье": 7}
    return sorted(checked, key=lambda x: (order.get(x["day"], 99), _to_minutes(x["start"])))

def main():
    lessons = [
        {"day": "Понедельник", "start": "09:00", "end": "10:30", "room": "301", "subject": "Программирование"},
        {"day": "Понедельник", "start": "10:00", "end": "11:30", "room": "301", "subject": "Базы данных"},
        {"day": "Понедельник", "start": "10:00", "end": "11:30", "room": "205", "subject": "Математика"},
        {"day": "Вторник", "start": "12:00", "end": "13:30", "room": "301", "subject": "Сети"},
    ]
    lessons = sort_lessons(lessons)
    conflicts = find_conflicts(lessons)
    print("РАСПИСАНИЕ ЗАНЯТИЙ")
    print("=" * 60)
    for x in lessons:
        print(f"{x['day']}: {x['start']}-{x['end']} | {x.get('subject', 'Занятие')} | ауд. {x['room']}")
    print("\n" + format_conflicts(conflicts))

if __name__ == "__main__":
    main()
