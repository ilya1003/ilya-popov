"""Лабораторная работа №2: императивная парадигма. Вариант 15 — Такси."""


def task1():
    x = 10
    for operation in ('+5', '*2', '-8', '//2'):
        if operation == '+5':
            x = x + 5
        elif operation == '*2':
            x = x * 2
        elif operation == '-8':
            x = x - 8
        else:
            x = x // 2
        print(f'{operation}: x = {x}')
    return x


def task2(price, quantity, discount_percent):
    if price < 0 or quantity < 0 or not 0 <= discount_percent <= 100:
        raise ValueError('Некорректные данные покупки')
    subtotal = price * quantity
    discount = subtotal * discount_percent / 100
    total = subtotal - discount
    return subtotal, discount, total


def task3(score):
    if not 0 <= score <= 100:
        return 'Ошибка: балл должен быть от 0 до 100'
    if score >= 90:
        return 'A'
    elif score >= 75:
        return 'B'
    elif score >= 50:
        return 'C'
    else:
        return 'F'


def task4():
    numbers = [12, -5, 8, -3, 21, 0, 14, -7]
    total = 0
    positive_sum = 0
    positive_count = 0
    negative_count = 0
    zero_count = 0
    for number in numbers:
        total = total + number
        if number > 0:
            positive_sum = positive_sum + number
            positive_count = positive_count + 1
        elif number < 0:
            negative_count = negative_count + 1
        else:
            zero_count = zero_count + 1
        print(f'Число: {number}, текущая сумма: {total}')
    return total, positive_sum, positive_count, negative_count, zero_count


def task5():
    scores = [67, 82, 45, 91, 76, 88, 54]
    maximum = scores[0]
    for score in scores:
        before = maximum
        if score > maximum:
            maximum = score
        print(f'Число: {score}, максимум до: {before}, после: {maximum}')
    return maximum


def taxi_fare(distance):
    """Посадка 500 тг, 120 тг/км, скидка 5% при distance > 20 км."""
    if distance < 0:
        raise ValueError('Расстояние не может быть отрицательным')
    subtotal = 500 + 120 * distance
    discount = 0
    if distance > 20:
        discount = subtotal * 0.05
    final_price = subtotal - discount
    return subtotal, discount, final_price


def comparison():
    numbers = [-4, 7, -2, 10, 5, -8]
    total = 0
    for number in numbers:
        if number > 0:
            total = total + number
            print(f'Императивный накопитель: {total}')
    declarative_total = sum(number for number in numbers if number > 0)
    return total, declarative_total


def main():
    print('Лабораторная работа № 2 — вариант 15 «Такси»')
    print('\nЗадание 1:')
    print('Результат:', task1())
    print('\nЗадание 2:')
    price = float(input('Цена товара: '))
    quantity = int(input('Количество товаров: '))
    discount_percent = float(input('Скидка (%): '))
    print('Без скидки, скидка, к оплате:', task2(price, quantity, discount_percent))
    print('\nЗадание 3:')
    score = float(input('Балл (0–100): '))
    print('Оценка:', task3(score))
    print('\nЗадание 4:')
    print('Итоги:', task4())
    print('\nЗадание 5:')
    print('Максимум:', task5())
    print('\nИндивидуальное задание № 15 — Такси:')
    distance = float(input('Введите расстояние поездки (км): '))
    subtotal, discount, final_price = taxi_fare(distance)
    print(f'Стоимость до скидки: {subtotal:.2f} тг')
    print(f'Скидка: {discount:.2f} тг')
    print(f'К оплате: {final_price:.2f} тг')
    print('\nСравнительное задание:', comparison())


if __name__ == '__main__':
    main()
