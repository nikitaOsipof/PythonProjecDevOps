import csv
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ValidationError

class Transaction(BaseModel):
    id: int
    # Pydantic сам распарсит стандартные форматы даты
    timestamp: datetime
    # Валидация суммы: должна быть положительной
    amount: float = Field(gt=0)
    # Опциональное поле, если в CSV пусто — будет None
    category: Optional[str] = "unknown"

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_custom_date(cls, v):
        # Если дата пришла в нестандартном формате (напр. DD/MM/YYYY)
        if isinstance(v, str) and "/" in v:
            return datetime.strptime(v, "%d/%m/%Y")
        return v

# Имитация чтения CSV
raw_data = [
    {"id": "1", "timestamp": "2023-10-01 12:00", "amount": "150.50", "category": "food"},
    {"id": "2", "timestamp": "25/12/2023", "amount": "42", "category": ""}, # Кастомная дата
    {"id": "3", "timestamp": "invalid", "amount": "-10"} # Ошибочная строка
]

valid_records = []
errors = []
for row in raw_data:
    try:
        # Валидация и приведение типов (Coercion)
        valid_records.append(Transaction(**row))
    except ValidationError as e:
        errors.append({"row": row, "error": e.errors()})

print(f"Успешно загружено: {len(valid_records)}")
print(f"Ошибок: {len(errors)}")
