import yaml

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Python видит это как обычный словарь:
print(config["api_server"]["host"])     # Выведет: 127.0.0.1
print(config["web_server"]["logging"])  # Выведет: DEBUG
