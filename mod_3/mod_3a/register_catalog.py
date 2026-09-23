'''
Сценарий: есть множество таблиц в слое Staging.
Требуется, чтобы при объявлении нового класса таблицы он автоматически регистрировался в глобальном реестре пайплайна
(Data Catalog), чтобы движок оркестрации знал о его существовании
'''
# Глобальный реестр DWH-моделей
dwh_catalog = {}


# Функция-декоратор для КЛАССОВ
def register_dwh_model(table_name):
    def class_decorator(cls):
        # Добавляем классу метаданные
        cls.target_table = table_name

        # Регистрируем класс-объект в нашем каталоге
        dwh_catalog[table_name] = cls

        # Возвращаем класс обратно без изменений
        return cls

    return class_decorator


# Применяем декоратор к КЛАССАМ
@register_dwh_model(table_name="stg_users")
class UsersModel:
    def transform(self, df):
        return df.dropna()


@register_dwh_model(table_name="stg_orders")
class OrdersModel:
    def transform(self, df):
        return df.fillna(0)


# --- Проверяем работу реестра в движке пайплайна ---
print("Зарегистрированные в DWH таблицы:")
for table, class_obj in dwh_catalog.items():
    # class_obj — это полноценный класс, сохраненный как объект!
    print(f"Таблица: {table} -> Связанный класс-парсер: {class_obj.__name__}")
