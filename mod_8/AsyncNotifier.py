import asyncio


class BaseAsyncNotifier:
    async def send_report(self, report_text: str):
        pass


class MockAsyncTelegramNotifier(BaseAsyncNotifier):
    """Безопасный асинхронный нотификатор для демонстрации и тестов."""

    def __init__(self, chat_ids: list):
        self.chat_ids = chat_ids

    async def _send_to_one_chat(self, chat_id, text):
        # Вместо реального HTTP-запроса имитируем задержку сети в 1 секунду
        # В этот момент поток освобождается для других чатов!
        await asyncio.sleep(1.0)
        print(f"[Mock-Успех] Отчет отправлен в чат {chat_id}")
        return 200

    async def send_report(self, report_text: str):
        print(f"Начинаем параллельную отправку в {len(self.chat_ids)} чатов...")

        # Создаем список асинхронных задач
        tasks = [
            self._send_to_one_chat(chat_id, report_text)
            for chat_id in self.chat_ids
        ]

        # Запускаем все задачи одновременно
        start_time = asyncio.get_event_loop().time()
        await asyncio.gather(*tasks)
        end_time = asyncio.get_event_loop().time()

        print(f"Все уведомления отправлены за {end_time - start_time:.2f} сек.!")


async def main():
    # Симулируем отправку сразу в 10 чатов
    chats = [f"chat_id_{i}" for i in range(10)]
    notifier = MockAsyncTelegramNotifier(chat_ids=chats)

    await notifier.send_report("Критическая ошибка на PROD-сервере!")


if __name__ == "__main__":
    asyncio.run(main())
