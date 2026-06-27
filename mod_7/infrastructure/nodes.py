import logging

logger = logging.getLogger(__name__)


class Server:

    def __init__(self, hostname, ip):
        self.hostname = hostname
        self.ip = ip

    def __str__(self):
        return f"Сервер: {self.hostname} [IP: {self.ip}]"


class WebServer(Server):

    def __init__(self, hostname, ip, port=80):
        # Инициализируем родительские атрибуты
        super().__init__(hostname, ip)
        # Добавляем специфичный для веб-сервера атрибут
        self.port = port

    def get_monitoring_url(self):
        return f"http://{self.ip}:{self.port}/health"
