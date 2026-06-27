# Импортируем классы из нашего пакета
from infrastructure.nodes import Server, WebServer

if __name__ == "__main__":
    print("--- Создание базового сервера ---")
    base_srv = Server("db-replica-01", "10.0.0.4")
    # Проверка работы dunder-метода __str__
    print(base_srv)

    print("\n--- Создание Веб-сервера (Наследование) ---")
    web_srv = WebServer("nginx-frontend", "192.168.1.100", port=443)

    # Веб-сервер должен корректно выводить свою базовую информацию
    print(web_srv)

    # Проверка работы уникального метода дочернего класса
    print("URL мониторинга:", web_srv.get_monitoring_url())
