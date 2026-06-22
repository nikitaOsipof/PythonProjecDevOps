'''
Контрольное задание вместо 4В
Напишете код, который находит все yaml файлы в проекте, проверяет, не пустые ли они, и загружает их настройки
и загрузите в файл json или yaml
Добавьте код в указанные места
'''
from pathlib import Path
import yaml
import json

search_dir = '.' # путь к папке вашего проекта
combined_settings = {}
dir_path = Path(search_dir)

# Ищем все файлы yaml рекурсивно
for file in '''ваш код''':
    # Проверяем, что это файл и он не пустой (размер в байтах > 0)
    if '''ваш код''' > 0:
        with open(file, "r", encoding="utf-8") as f:
            # Используем имя файла без расширения в качестве ключа
            '''ваш код'''

print(combined_settings)
# Запись данных в JSON-файл
with open("combined_settings.json", "w", encoding="utf-8") as file:
    json.dump('''ваш код''')

# Запись в YAML-файл
with open("combined_settings.yaml", "w", encoding="utf-8") as file:
    yaml.safe_dump('''ваш код''')