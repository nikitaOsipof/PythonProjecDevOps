import itertools
import time


# --- (Чанкер-батчер) ---
def batch_stream(iterable, batch_size):
    iterator = iter(iterable)
    while True:
        # Код заблокируется здесь, пока не соберет ВСЕ элементы до batch_size
        batch = list(itertools.islice(iterator, batch_size))
        if not batch:
            break
        yield batch


# --- СИМУЛЯЦИЯ ЖИВОГО ПОТОКА ДАННЫХ ---
def live_network_stream():
    """Имитирует приток кликов с сайта: днем активно, ночью — затишье."""
    print("[STREAM] --- День: Пошли активные клики ---")
    yield {"click_id": 1, "time": "14:00:01"}
    yield {"click_id": 2, "time": "14:00:02"}
    yield {"click_id": 3, "time": "14:00:03"}

    print("\n[STREAM] --- Ночь: Наступило затишье. Ждем 3 секунды... ---")
    time.sleep(3)  # Имитация долгого ожидания в сети

    yield {"click_id": 4, "time": "03:15:00"}  # Ночной клик

    print("\n[STREAM] --- Утро следующего дня: Пошли новые клики ---")
    yield {"click_id": 5, "time": "09:00:01"}
    yield {"click_id": 6, "time": "09:00:02"}


# --- ЗАПУСК ТЕСТА ---
if __name__ == "__main__":
    # Настраиваем размер пачки = 4 элемента
    # Мы хотим, чтобы база данных получала накопленные клики
    batches = batch_stream(live_network_stream(), batch_size=4)

    print("Старт обработки потока через islice...\n")

    start_time = time.time()
    for chunk in batches:
        elapsed = time.time() - start_time
        print(f" [БАЗА ДАННЫХ] Получен батч через {elapsed:.1f} сек от старта! Содержимое:")
        for item in chunk:
            print(f"   -> Клиент кликнул в {item['time']}")
