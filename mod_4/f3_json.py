'''JSON — это текстовый формат, но Python умеет автоматически превращать его структуры во встроенные
 словари (dict) и списки (list).
Для этого используется стандартный модуль json.'''

import json

data = {
    "user_id": 42,
    "username": "Niko",
    "is_active": True,
    "skills": ["Python", "Docker"]
}

# Запись данных в JSON-файл
with open("config.json", "w", encoding="utf-8") as file:
    # ensure_ascii=False сохраняет кириллицу как текст, а не как \u043f...
    # indent=4 делает красивые отступы в файле
    json.dump(data, file, ensure_ascii=False, indent=4)

# Чтение из JSON-файла обратно в Python-словарь
with open("config.json", "r", encoding="utf-8") as file:
    loaded_data = json.load(file)
    print(loaded_data["username"])  # Выведет: Niko

# dumps - преобразует объект python в строку json
json_str = json.dumps(data, ensure_ascii=False, indent=4)

print(json_str)