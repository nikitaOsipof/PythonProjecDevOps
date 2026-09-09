from abc import ABC, abstractmethod
from typing import Optional, Type

# 1. Абстрактный базовый класс (Интерфейс коннектора к хранилищу)
class BaseStorageTarget(ABC):
    def __init__(self, target_uri: str):
        self.target_uri = target_uri

    @abstractmethod
    def open_session(self) -> None:
        """Каждое хранилище должно по-своему открыть сессию записи"""
        pass

    @abstractmethod
    def write_record(self, message: str) -> None:
        """Каждое хранилище реализует свою логику записи"""
        pass

    @abstractmethod
    def close_session(self, is_success: bool) -> None:
        """Каждое хранилище по-своему финализирует сессию"""
        pass

    # Интеграция с темой контекстных менеджеров:
    def __enter__(self):
        self.open_session()
        return self

    def __exit__(
        self, 
        exc_type: Optional[Type[BaseException]], 
        exc_val: Optional[BaseException], 
        exc_tb: Optional[object]
    ) -> bool:
        # Если exc_type равен None, значит код внутри with выполнился успешно
        success = exc_type is None
        self.close_session(is_success=success)
        return False  # Ошибки не подавляем, пробрасываем выше


# 2. Конкретная реализация №1: Локальное файловое хранилище (для разработки)
class LocalFileStorage(BaseStorageTarget):
    def __init__(self, target_uri: str):
        super().__init__(target_uri)
        self.file = None

    def open_session(self) -> None:
        file_path = self.target_uri.replace("file://", "")
        print(f"[Файл] Открываем локальный файл для записи: {file_path}")
        self.file = open(file_path, "a", encoding="utf-8")
        self.file.write("--- Старт локальной сессии ---\n")

    def write_record(self, message: str) -> None:
        if self.file:
            self.file.write(f"[DATA] {message}\n")

    def close_session(self, is_success: bool) -> None:
        if self.file:
            status = "УСПЕХ" if is_success else "СБОЙ"
            self.file.write(f"--- Конец локальной сессии Статус: {status} ---\n\n")
            self.file.close()
            print("[Файл] Локальный файл успешно закрыт.")


# 3. Конкретная реализация №2: Удаленный сервер сбора логов (для продакшена)
class RemoteNetworkStorage(BaseStorageTarget):
    def open_session(self) -> None:
        print(f"[Сеть] Устанавливаем TCP-соединение с сервером: {self.target_uri}")
        print("[Сеть] Сессия мониторинга успешно открыта.")

    def write_record(self, message: str) -> None:
        # Имитация отправки сетевых пакетов
        print(f"[Сеть] Отправка пакета на удаленный сервер: {message}")

    def close_session(self, is_success: bool) -> None:
        if is_success:
            print("[Сеть] Отправлен финальный пакет успешного завершения.")
        else:
            print("[Сеть] ! Внимание ! Отправлен экстренный сигнал тревоги.")
        print("[Сеть] Сетевой сокет закрыт. Сессия завершена.")


# 4. Класс-Фабрика (Выбирает класс хранилища на основе префикса URI)
class StorageFactory:
    @staticmethod
    def create_target(connection_string: str) -> BaseStorageTarget:
        if connection_string.startswith("file://"):
            return LocalFileStorage(connection_string)
        elif connection_string.startswith("http://") or connection_string.startswith("https://"):
            return RemoteNetworkStorage(connection_string)
        else:
            raise ValueError(f"Неизвестный тип хранилища: {connection_string}")


# 5. Код пайплайна (Абстрагирован от того, КУДА пишутся данные)
def run_ingestion_job(storage_uri: str):
    print(f"\nИнициализация пайплайна. Целевой таргет: {storage_uri}")
    
    # Фабрика возвращает объект общего интерфейса BaseStorageTarget
    storage = StorageFactory.create_target(storage_uri)
    
    with storage as target:
        target.write_record("Запущена валидация чанка данных")
        target.write_record("Обработано 150 строк без ошибок")
        
        # Симулируем непредвиденную ошибку на проде (для проверки close_session)
        if "prod-server" in storage_uri:
            print("[Пайплайн] Ошибка: Переполнение буфера!")
            raise BufferError("Недостаточно места")


if __name__ == "__main__":
    # Локальный тест (Запишет данные в файл)
    try:
        run_ingestion_job("file://pipeline_debug.log")
    except Exception:
        pass

    # Продакшн запуск (Отправит данные в сеть и вызовет сигнал тревоги при сбое)
    try:
        run_ingestion_job("http://company.internal")
    except Exception:
        pass
