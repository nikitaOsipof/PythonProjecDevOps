'''
Бинарные файлы считываются не как текст, а как поток сырых байт (тип данных bytes).
Для работы с ними к режимам чтения и записи добавляется буква b ('rb' или 'wb'
'''
# Чтение картинки в байты
with open("Bill Gates.jpg", "rb") as source_file:
    byte_data = source_file.read()
    # На экране мы увидим что-то вроде b'\x89PNG\r\n\x1a\n...'
    print(byte_data[:10])

# Копирование (запись) бинарного файла
with open("copy_avatar.jpg", "wb") as target_file:
    target_file.write(byte_data)
