# Пайплайн очистки и трансформации логов
'''
Задача. Дан грязный поток логов. Требуется:
1.	Прочитать строки (Имитируем чтение файла).
2.	Очистить строки от лишних пробелов и символов переноса строки.
3.	Отфильтровать только критические ошибки (CRITICAL).
4.	Распарсить их в формат словаря для последующей отправки в базу данных.
'''

# --- ЗВЕНО 1: ИСТОЧНИК (Генератор строк) ---
def read_raw_logs():
    """ Имитирует чтение гигантского 100 ГБ файла по одной строке """
    raw_data = [
        "  USER_LOGIN: user_101  \n",
        "  CRITICAL: Database connection failed!  \n", # Наша цель
        "  INFO: Subsystem initialized  \n",
        "  CRITICAL: Out of Memory detected!  \n",     # Наша цель
        "  DEBUG: Execution time 12ms  \n"
    ]
    for line in raw_data:
        yield line


# --- ЗВЕНО 2: ТРАНСФОРМАЦИЯ (Очистка) ---
def clean_lines(lines_stream):
    """ Принимает поток строк, удаляет пробелы по краям """
    for line in lines_stream:
        print(f"[Конвейер -> Шаг 2] Очищаю строку: '{line.strip()}'")
        yield line.strip()


# --- ЗВЕНО 3: ФИЛЬТРАЦИЯ (Выбор ошибок) ---
def filter_errors(cleaned_stream):
    """ Принимает очищенный поток, пропускает только CRITICAL """
    for line in cleaned_stream:
        if line.startswith("CRITICAL:"):
            print(f"[Конвейер -> Шаг 3] Найдена критическая ошибка!")
            yield line


# --- ЗВЕНО 4: ПАРСИНГ (Структурирование) ---
def parse_to_dict(error_stream):
    """ Превращает текст ошибки в структурированный словарь """
    for line in error_stream:
        payload = line.replace("CRITICAL:", "").strip()
        print(f"[Конвейер -> Шаг 4] Парсю в словарь")
        yield {"status": "CRITICAL", "message": payload}

# --- СБОРКА И ЗАПУСК ПАЙПЛАЙНА ---

# Соединяем звенья друг за другом.
# На этом этапе данные ЕЩЕ НЕ НАЧАЛИ обрабатываться. Память абсолютно пуста!
stage_1 = read_raw_logs()
stage_2 = clean_lines(stage_1)
stage_3 = filter_errors(stage_2)
pipeline = parse_to_dict(stage_3)

print("🚀 Пайплайн собран. Начинаем извлечение данных поштучно:\n")

# Запускаем конвейер. Цикл for начинает вызывать метод next() у финального звена [см. выше].
for final_result in pipeline:
    print(f"🔥 РЕЗУЛЬТАТ НА ВЫХОДЕ: {final_result}")
    print("-" * 50)
