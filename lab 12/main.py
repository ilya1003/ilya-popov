"""Лабораторная работа №12. Вариант 8 — уведомления студентам.

Асинхронный конвейер отправки уведомлений с ограниченной очередью,
двумя потребителями и повторными попытками с экспоненциальной задержкой.
Python 3.11+
"""
from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any

SENTINEL = object()


@dataclass
class Notification:
    address: str
    subject: str
    message: str
    fail_attempts: int = 0  # Учебная имитация временных ошибок сервиса.


def validate(notification: Notification) -> None:
    """Проверяет обязательные поля уведомления."""
    if not notification.address.strip():
        raise ValueError("Не указан адрес получателя")
    if "@" not in notification.address or notification.address.startswith("@"):
        raise ValueError("Некорректный адрес получателя")
    if not notification.subject.strip():
        raise ValueError("Не указана тема уведомления")
    if not notification.message.strip():
        raise ValueError("Пустой текст уведомления")
    if notification.fail_attempts < 0:
        raise ValueError("Количество временных ошибок не может быть отрицательным")


async def send_notification(
    notification: Notification,
    attempt: int,
    delay: float = 0.05,
) -> None:
    """Имитирует асинхронную отправку уведомления."""
    await asyncio.sleep(delay)
    if attempt <= notification.fail_attempts:
        raise ConnectionError("Временная ошибка сервиса отправки")


async def deliver(
    notification: Notification,
    max_retries: int = 3,
    base_delay: float = 0.05,
) -> int:
    """Отправляет уведомление; возвращает число выполненных попыток."""
    validate(notification)
    for attempt in range(1, max_retries + 2):
        try:
            await send_notification(notification, attempt)
            return attempt
        except ConnectionError:
            if attempt > max_retries:
                raise
            # Экспоненциальная задержка: 0.05, 0.10, 0.20 ... секунды.
            await asyncio.sleep(base_delay * (2 ** (attempt - 1)))
    raise RuntimeError("Недостижимая ветвь")


async def producer(queue: asyncio.Queue, notifications: list[Notification]) -> None:
    """Помещает уведомления в ограниченную очередь."""
    for notification in notifications:
        await asyncio.sleep(0.02)  # Имитация поступления заявки.
        await queue.put(notification)
        print(f"Добавлено в очередь: {notification.address}")
    # По одному сигналу завершения для каждого потребителя.
    for _ in range(2):
        await queue.put(SENTINEL)


async def consumer(
    name: str,
    queue: asyncio.Queue,
    sent: list[dict[str, Any]],
    errors: list[str],
    attempts: list[int],
) -> None:
    """Получает уведомления и обрабатывает их независимо от других работников."""
    while True:
        item = await queue.get()
        try:
            if item is SENTINEL:
                print(f"{name}: завершение работы")
                return
            try:
                used_attempts = await deliver(item)
                sent.append({
                    "address": item.address,
                    "subject": item.subject,
                    "attempts": used_attempts,
                    "status": "отправлено",
                })
                attempts.append(used_attempts)
                print(f"{name}: отправлено на {item.address} "
                      f"(попыток: {used_attempts})")
            except (ValueError, ConnectionError) as error:
                errors.append(f"{item.address}: {error}")
                print(f"{name}: ошибка для {item.address}: {error}")
        finally:
            # Вызывается для каждого извлечённого элемента, включая SENTINEL.
            queue.task_done()


async def run_pipeline(
    notifications: list[Notification],
) -> dict[str, Any]:
    """Запускает конвейер и возвращает итоговую статистику."""
    queue: asyncio.Queue = asyncio.Queue(maxsize=3)
    sent: list[dict[str, Any]] = []
    errors: list[str] = []
    attempts: list[int] = []
    started = time.perf_counter()

    workers = [
        asyncio.create_task(
            consumer(f"worker-{number}", queue, sent, errors, attempts)
        )
        for number in range(1, 3)
    ]

    await producer(queue, notifications)
    await queue.join()
    await asyncio.gather(*workers)

    elapsed = time.perf_counter() - started
    return {
        "sent": sent,
        "errors": errors,
        "sent_count": len(sent),
        "error_count": len(errors),
        "average_attempts": sum(attempts) / len(attempts) if attempts else 0.0,
        "elapsed": elapsed,
    }


def print_report(stats: dict[str, Any]) -> None:
    """Печатает краткий отчёт."""
    print("\n========== ИТОГОВЫЙ ОТЧЁТ ==========")
    print(f"Успешно отправлено: {stats['sent_count']}")
    print(f"Ошибок: {stats['error_count']}")
    print(f"Среднее число попыток: {stats['average_attempts']:.2f}")
    print(f"Время выполнения: {stats['elapsed']:.2f} сек.")
    for error in stats["errors"]:
        print(f"Ошибка: {error}")


async def main() -> None:
    notifications = [
        Notification("aliya@example.com", "Расписание", "Занятие начнётся в 09:00."),
        Notification("damir@example.com", "Дедлайн", "Сдать лабораторную до пятницы.",
                     fail_attempts=2),
        Notification("ruslan@example.com", "Экзамен", "Экзамен состоится 25 ноября."),
        Notification("", "Объявление", "Тестовая запись с ошибкой."),
        Notification("madina@example.com", "", "Тестовая запись с ошибкой."),
        Notification("arina@example.com", "Встреча", "Собрание в 14:00.",
                     fail_attempts=5),  # Превышен лимит повторов.
    ]

    stats = await run_pipeline(notifications)
    print_report(stats)


if __name__ == "__main__":
    asyncio.run(main())
