from pathlib import Path

# 1. Создаем базовый путь (например, к папке проекта)
# Path(".") означает текущую директорию
base_dir = Path(".")

# 2. Склеиваем путь к файлу внутри папок src/my_app/
# Python сам поймет, какая у вас ОС, и поставит правильные слэши!
config_path = base_dir / "src" / "my_app" / "config.json"

print(config_path)
# На Windows выведет: src\my_app\config.json
# На Linux/Docker выведет: src/my_app/config.json

# 3. Динамическое определение путей
# Получаем абсолютный путь к файлу, в котором написан этот код
current_file = Path(__file__).resolve()
print(f"Путь к скрипту: {current_file}")

# Получаем папку, в которой лежит этот скрипт (.parent)
current_dir = current_file.parent
print(f"Папка скрипта: {current_dir}")

# Ищем файл settings.yaml, который лежит на одну папку выше (в корне проекта)
# .parent.parent означает "выйти на два уровня вверх"
root_dir = current_file.parent.parent.parent
config_file = root_dir / "settings.yaml"
print(config_file)

# 4. Информация объекта пути о файле
path = Path("src/my_app/data.csv")

print(path.name)      # data.csv  (полное имя)
print(path.stem)      # data      (имя без расширения)
print(path.suffix)    # .csv      (только расширение)
print(path.parts)     # ('src', 'my_app', 'data.csv') (компоненты пути)

# Проверки (возвращают True или False)
print(path.exists())  # Существует ли такой файл/папка вообще?
print(path.is_file()) # Это файл?
print(path.is_dir())  # Это папка?
