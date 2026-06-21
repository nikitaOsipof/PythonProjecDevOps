'''Текстовые файлы считываются как обычные строки.
При работе с текстом всегда явно указывайте кодировку encoding="utf-8"'''


# Запись в текстовый файл (режим 'w' - write, перезапишет файл)
with open("example.txt", "w", encoding="utf-8") as file:
    file.write("Привет, Python!\n")
    file.write("Вторая строка.")

# Чтение текстового файла целиком
with open("example.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)

# Pythonic: Чтение файла построчно (генератор, не забивает память)
with open("example.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())  # strip() убирает скрытый символ переноса строки \n
