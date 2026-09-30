from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator


class DroneTelemetrySchema(BaseModel):
    """
    Декларативная схема Pydantic для проверки бортовых параметров дрона.
    """
    drone_id: str = Field(min_length=5, description="Уникальный код аппарата")
    speed_mps: float = Field(ge=0.0, le=100.0, description="Скорость в метрах в секунду")
    battery_percentage: int = Field(ge=0, le=100)
    gps_coordinates: List[float] = Field(min_length=2, max_length=2, description="[Широта, Долгота]")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # 1. Валидатор конкретного поля (Field Validator)
    @field_validator("drone_id")
    @classmethod
    def validate_and_clean_id(cls, value: str) -> str:
        # Убираем случайные пробелы и принудительно переводим в верхний регистр
        cleaned_id = value.strip().upper()
        if not cleaned_id.startswith("DRONE_"):
            raise ValueError("Идентификатор аппарата должен строго начинаться с префикса 'DRONE_'")
        return cleaned_id

    # 2. Валидатор всей модели (Model Validator)
    @model_validator(mode="after")
    def check_safety_rules(self) -> "DroneTelemetrySchema":
        # Бизнес-правило: если батарея почти разряжена (меньше 10%), скорость должна быть снижена до безопасной
        if self.battery_percentage < 10 and self.speed_mps > 15.0:
            raise ValueError(
                f"Критический уровень заряда ({self.battery_percentage}%). "
                f"Скорость {self.speed_mps} м/с превышает аварийный лимит в 15.0 м/с!"
            )
        return self


# --- Код симуляции обработки потока данных на лекции ---
if __name__ == "__main__":
    print("--- Инициализация шлюза приема телеметрии ---")

    # Пример 1: Идеальный пакет с датчиков (Pydantic сам распарсит дату из строки)
    valid_packet = {
        "drone_id": "   drone_quad_42   ",
        "speed_mps": 25.4,
        "battery_percentage": 85,
        "gps_coordinates": [55.7558, 37.6173],
        "timestamp": "2026-07-05T14:30:00"
    }

    parsed_drone = DroneTelemetrySchema(**valid_packet)
    print(f"[УСПЕХ] Данные приняты. Очищенный ID: {parsed_drone.drone_id}")
    print(f"Дата в формате Python datetime: {type(parsed_drone.timestamp)} -> {parsed_drone.timestamp}\n")

    # Пример 2: Пакет с критическими ошибками
    corrupted_packet = {
        "drone_id": "bad_quad_01",  # Ошибка: нет префикса DRONE_
        "speed_mps": 35.0,
        "battery_percentage": 5,  # Ошибка: при батарее 5% скорость 35 м/с запрещена валидатором модели
        "gps_coordinates": [55.75]  # Ошибка: пропущена одна координата
    }

    try:
        DroneTelemetrySchema(**corrupted_packet)
    except ValidationError as e:
        print("[ОТКЛОНЕНО] Обнаружен брак данных! Лог ошибок Pydantic:")
        # Выводим структурированный JSON с детальным описанием ошибок
        print(e.json(indent=2))
