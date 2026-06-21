import  yaml
from pathlib import Path

# Указываем стартовую папку для поиска (например, корень проекта)
project_root = Path(".")

# Метод .rglob("*.yaml") возвращает генератор (ленивый обход диска)
# Он найдет config.yaml, settings.yaml и файлы глубоко внутри папок
yaml_files = project_root.rglob("*.yaml")

print("Найденные файлы конфигураций:")
for file_path in yaml_files:
    # file_path — это полноценный объект Path, у него есть все методы
    print(f"-> Найдено: {file_path.name} по пути: {file_path}")

    # Можно тут же открыть его и прочитать!
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
