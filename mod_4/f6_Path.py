from pathlib import Path

# Автоматическое создание папок

# Задаем путь к будущему файлу
log_dir = Path("logs") / "archive"
log_file = log_dir / "app.log"

# Создаем всю цепочку папок, если их еще нет
# parents=True создаст и logs, и archive
# exist_ok=True не будет ругаться, если папка уже существует
log_dir.mkdir(parents=True, exist_ok=True)

# Теперь можно безопасно открывать файл на запись
with open(log_file, "w", encoding="utf-8") as f:
    f.write("Лог записан.")

# с функцией open()
my_file = Path("settings.yaml")

# Передаем объект пути прямо в with open
with open(my_file, "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

# с созданным ранее логом
with open(log_file, "r", encoding="utf-8") as f:
    content = f.read()
    print(content)