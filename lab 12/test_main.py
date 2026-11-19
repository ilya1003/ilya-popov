"""Автоматические тесты для лабораторной работы №12, вариант 8."""
import asyncio
import unittest

from main import (
    Notification,
    deliver,
    run_pipeline,
    validate,
)


class ValidationTests(unittest.TestCase):
    def test_valid_notification(self):
        validate(Notification("student@example.com", "Тема", "Текст"))

    def test_empty_address(self):
        with self.assertRaisesRegex(ValueError, "Не указан адрес"):
            validate(Notification("", "Тема", "Текст"))

    def test_invalid_address(self):
        with self.assertRaisesRegex(ValueError, "Некорректный адрес"):
            validate(Notification("student.example.com", "Тема", "Текст"))

    def test_empty_subject(self):
        with self.assertRaisesRegex(ValueError, "Не указана тема"):
            validate(Notification("student@example.com", " ", "Текст"))

    def test_empty_message(self):
        with self.assertRaisesRegex(ValueError, "Пустой текст"):
            validate(Notification("student@example.com", "Тема", " "))

    def test_negative_fail_attempts(self):
        with self.assertRaisesRegex(ValueError, "отрицательным"):
            validate(Notification("student@example.com", "Тема", "Текст", -1))


class AsyncPipelineTests(unittest.IsolatedAsyncioTestCase):
    async def test_success_without_retry(self):
        attempts = await deliver(
            Notification("a@example.com", "Тема", "Текст"),
            base_delay=0.001,
        )
        self.assertEqual(attempts, 1)

    async def test_success_after_retries(self):
        attempts = await deliver(
            Notification("a@example.com", "Тема", "Текст", fail_attempts=2),
            max_retries=3,
            base_delay=0.001,
        )
        self.assertEqual(attempts, 3)

    async def test_retry_limit_exceeded(self):
        with self.assertRaises(ConnectionError):
            await deliver(
                Notification("a@example.com", "Тема", "Текст", fail_attempts=5),
                max_retries=2,
                base_delay=0.001,
            )

    async def test_pipeline_collects_success_and_errors(self):
        stats = await run_pipeline([
            Notification("a@example.com", "Тема", "Текст"),
            Notification("", "Тема", "Текст"),
        ])
        self.assertEqual(stats["sent_count"], 1)
        self.assertEqual(stats["error_count"], 1)

    async def test_empty_input(self):
        stats = await run_pipeline([])
        self.assertEqual(stats["sent_count"], 0)
        self.assertEqual(stats["error_count"], 0)
        self.assertEqual(stats["average_attempts"], 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
