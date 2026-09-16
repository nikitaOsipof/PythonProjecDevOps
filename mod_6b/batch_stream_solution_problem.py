import asyncio
import time


# --- АСИНХРОННЫЙ РЕАЛТАЙМ-БАТЧЕР ---
async def batch_stream_async(queue: asyncio.Queue, batch_size: int, timeout: float):
    """Лениво собирает элементы из очереди.

    Сбрасывает пачку при достижении лимита размера ИЛИ по таймауту.
    """
    batch = []
    # Засекаем время дедлайна для текущего батча
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout

    while True:
        try:
            # Считаем, сколько времени осталось до таймаута
            time_left = deadline - loop.time()

            # Если время уже вышло, принудительно выходим из ожидания очереди
            if time_left <= 0:
                raise asyncio.TimeoutError()

            # Ждем элемент из очереди, но не дольше, чем осталось времени до таймаута
            item = await asyncio.wait_for(queue.get(), timeout=time_left)
            batch.append(item)
            queue.task_done()

            # Триггер 1: Набрали нужный размер — отдаем батч
            if len(batch) >= batch_size:
                yield batch
                batch = []
                deadline = loop.time() + timeout  # Обнуляем таймер

        except asyncio.TimeoutError:
            # Триггер 2: Сработал таймаут, а пачка не полная — все равно отдаем!
            if batch:
                yield batch
                batch = []
            # Сбрасываем таймер для следующей пачки
            deadline = loop.time() + timeout


# --- СИМУЛЯЦИЯ ПОТОКА КЛИКОВ (PUSH-модель) ---
async def live_data_producer(queue: asyncio.Queue):
    """Имитирует активность пользователей на сайте."""
    print("[STREAM] --- День: Пошли 3 быстрых клика ---")
    await queue.put({"click_id": 1, "time": "14:00:01"})
    await queue.put({"click_id": 2, "time": "14:00:02"})
    await queue.put({"click_id": 3, "time": "14:00:03"})

    print("[STREAM] --- Ночь: Затишье в сети на 3 секунды... ---")
    await asyncio.sleep(3)  # В это время сработает таймаут батчера!

    print("\n[STREAM] --- Ночной клик ---")
    await queue.put({"click_id": 4, "time": "03:15:00"})

    print("[STREAM] --- Утренние клики ---")
    await queue.put({"click_id": 5, "time": "09:00:01"})
    await queue.put({"click_id": 6, "time": "09:00:02"})


# --- ГЛАВНЫЙ КОНВЕЙЕР ОБРАБОТКИ ---
async def main():
    event_queue = asyncio.Queue()

    # Запускаем генератор кликов в фоне
    producer_task = asyncio.create_task(live_data_producer(event_queue))

    start_time = time.time()

    # Настраиваем батчер: пачка 4 элемента ИЛИ таймаут 1 секунда
    async for chunk in batch_stream_async(event_queue, batch_size=4, timeout=1.0):
        elapsed = time.time() - start_time
        print(f"\n [БАЗА ДАННЫХ] Получен батч через {elapsed:.1f} сек от старта!")
        for item in chunk:
            print(f"   -> Клиент кликнул в {item['time']} (ID: {item['click_id']})")

        # Останавливаем демо-скрипт, когда обработаем все 6 тестовых элементов
        if item['click_id'] == 6:
            break

    await producer_task


if __name__ == "__main__":
    asyncio.run(main())
