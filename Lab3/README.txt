Лабораторная работа №3 — Вариант 7
Тема: Расписание занятий.

Реализованы функции:
- validate_interval
- overlaps
- find_conflicts
- format_conflicts
- sort_lessons
- _to_minutes
- main

Есть проверка данных, поиск пересечений в одной аудитории,
сортировка и формирование текстового отчёта.
Учтён параметр break_minutes для обязательного перерыва.

Запуск в PyCharm:
1. Открыть папку проекта.
2. Запустить main.py.
3. Для тестов запустить test_main.py.

Через терминал:
python main.py
python -m unittest test_main.py -v
