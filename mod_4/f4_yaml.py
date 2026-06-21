'''
YAML файлы (Сложные конфигурации, как в Docker Compose)
Формат YAML удобнее для чтения человеком, чем JSON, и часто используется для настроек.
В отличие от JSON, поддержка YAML не встроена в Python «из коробки»:
добавьте в проект библиотеку PyYAML с помощью uv: uv add pyyaml
'''
import yaml

settings = {
    "server": {
        "host": "127.0.0.1",
        "port": 8080
    },
    "debug": False
}

# Запись в YAML-файл
with open("settings.yaml", "w", encoding="utf-8") as file:
    yaml.safe_dump(settings, file, default_flow_style=False, allow_unicode=True)

# Чтение из YAML-файла
with open("settings.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
    print(config["server"]["host"])  # Выведет: 127.0.0.1
