'''
Использование декораторов классов для валидации типов данных входящих строк (Data Quality Check)
 В Data Engineering важно отсекать «битые» данные до того, как они попадут в базу данных или тяжелый DataFrame.
Если мы пишем микро-ETL (например, парсер логов или обработчик вебхуков), тянуть огромные фреймворки бывает избыточно.
Вместо этого можно написать декоратор класса, который автоматически сверяет входящие данные со строгой аннотацией типов
самого класса (как это под капотом делает библиотека Pydantic).

Декоратор будет перехватывать процесс создания объекта класса (__init__),
сверять переданные в него типы данных с ожидаемыми аннотациями (__annotations__)
и при несовпадении выкидывать ошибку качества данных (ValueError).

'''
from functools import wraps


# Декоратор класса
def validate_data_schema(cls):
    # Получаем ожидаемые типы колонок из аннотаций класса
    # Например: {'user_id': int, 'email': str}
    expected_types = cls.__annotations__

    # Сохраняем оригинальный метод инициализации класса
    original_init = cls.__init__

    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        # Проверяем переданные именованные аргументы (нашу строку данных)
        for field_name, value in kwargs.items():
            if field_name in expected_types:
                expected_type = expected_types[field_name]

                # Проверяем, соответствует ли тип данных ожидаемому
                if not isinstance(value, expected_type):
                    raise ValueError(
                        f"[DATA QUALITY ERROR] Поле '{field_name}' ожидает тип {expected_type}, "
                        f"но получено значение '{value}' типа {type(value)}"
                    )

        # Если всё успешно, вызываем оригинальный __init__
        original_init(self, *args, **kwargs)

    # Подменяем оригинальный метод __init__ на наш валидатор
    cls.__init__ = new_init

    # Возвращаем модифицированный класс как объект первого класса
    return cls


'''
Применение в ETL-пайплайне
Теперь можем описать схему целевой таблицы DWH в виде чистого класса и защитить её одной строчкой:
'''


@validate_data_schema
class UserDWHRow:
    # Описываем строгий контракт данных (схему)
    user_id: int
    email: str
    is_active: bool

    def __init__(self, user_id, email, is_active):
        self.user_id = user_id
        self.email = email
        self.is_active = is_active


# --- Имитация работы пайплайна (разбор входящего потока данных) ---

good_row = {"user_id": 101, "email": "data_eng@test.com", "is_active": True}
bad_row = {"user_id": "NOT_AN_INT", "email": "hacker@test.com", "is_active": False}

# Сценарий 1: Валидные данные успешно создают объект строки DWH
try:
    row_obj = UserDWHRow(**good_row)
    print(f"[SUCCESS] Строка {row_obj.user_id} валидирована и готова к вставке.")
except ValueError as e:
    print(e)

# Сценарий 2: Невалидные данные перехватываются на лету
try:
    print("\nПробуем загрузить некорректную строку...")
    row_obj = UserDWHRow(**bad_row)
except ValueError as e:
    print(f"[BLOCKED] Загрузка заблокирована! Ошибка: {e}")
