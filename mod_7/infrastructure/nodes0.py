'''
Требуется:
Расширить созданный ранее пакет infrastructure.
Написать базовый класс для учета серверов, дочерний класс для веб-серверов с проверкой доступности,
и интегрировать их в общую логику пакета.
'''
import logging

# Используем логгер, настроенный в __init__.py
logger = logging.getLogger(__name__)


class Server:

    def __init__(self, hostname, ip):
        """
        Конструктор базового сервера.
        """
        self.hostname = hostname
        self.ip = ip

    def __str__(self):
        # TODO: Реализовать dunder-метод __str__
        # Он должен возвращать красивую строку вида: "Сервер: <hostname> [IP: <ip>]"
        pass


class WebServer(Server):

    def __init__(self, hostname, ip, port=80):
        """
        Конструктор веб-сервера. Должен наследовать hostname и ip от родительского класса.
        """
        # TODO: Используйте super() для вызова конструктора родительского класса Server
        # TODO: Сохраните порт в уникальный атрибут экземпляра
        pass

    def get_monitoring_url(self):
        """
        Возвращает URL-адрес для проверки здоровья (health check) веб-сервера.
        """
        # TODO: Вернуть строку в формате: http://<ip>:<port>/health
        pass
