"""Лабораторная работа № 5, вариант 14: оплата обучения."""
from dataclasses import dataclass
from datetime import datetime
from math import isfinite


def check_amount(amount):
    """Проверяет положительную сумму в тенге."""
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise TypeError('Сумма должна быть числом')
    if not isfinite(amount) or amount <= 0:
        raise ValueError('Сумма должна быть положительной и конечной')
    # Суммы хранятся в тиынах для точных денежных расчётов.
    cents = round(amount * 100)
    if abs(amount * 100 - cents) > 1e-7:
        raise ValueError('Не более двух знаков после запятой')
    return cents


@dataclass(frozen=True)
class Payment:
    """Неизменяемая запись операции со счётом студента."""
    operation: str
    amount_tiyin: int
    created_at: str

    @property
    def amount(self):
        """Возвращает сумму операции в тенге."""
        return self.amount_tiyin / 100


class StudentAccount:
    """Счёт студента: начисления, оплаты и история операций."""

    def __init__(self, student_id, student_name):
        if isinstance(student_id, bool) or not isinstance(student_id, int):
            raise TypeError('ID должен быть целым числом')
        if student_id <= 0:
            raise ValueError('ID должен быть положительным')
        if not isinstance(student_name, str) or not student_name.strip():
            raise ValueError('Имя студента не должно быть пустым')
        self.student_id = student_id
        self.student_name = student_name.strip()
        self._balance_tiyin = 0
        self._history = []

    @property
    def balance(self):
        """Текущий долг в тенге (не может быть отрицательным)."""
        return self._balance_tiyin / 100

    @property
    def history(self):
        """Возвращает неизменяемый снимок операций."""
        return tuple(self._history)

    def charge(self, amount):
        """Начисляет плату за обучение."""
        cents = check_amount(amount)
        self._balance_tiyin += cents
        self._history.append(Payment('Начисление', cents, datetime.now().isoformat(timespec='seconds')))

    def pay(self, amount):
        """Принимает оплату, запрещая переплату."""
        cents = check_amount(amount)
        if cents > self._balance_tiyin:
            raise ValueError('Оплата превышает текущий долг')
        self._balance_tiyin -= cents
        self._history.append(Payment('Оплата', cents, datetime.now().isoformat(timespec='seconds')))


def main():
    """Демонстрирует начисления, оплаты и историю счёта."""
    account = StudentAccount(101, 'Amina')
    account.charge(250000)
    account.pay(100000)
    account.charge(50000)
    account.pay(200000)
    print(f'Студент: {account.student_name} (ID {account.student_id})')
    print('История операций:')
    for operation in account.history:
        print(f'{operation.operation}: {operation.amount:.2f} тг')
    print(f'Текущий баланс (долг): {account.balance:.2f} тг')


if __name__ == '__main__':
    main()
