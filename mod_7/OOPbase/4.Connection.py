'''
Чтобы объект вашего класса можно было открывать через with, внутри класса надо написать два специальных метода enter и exit
Полезно применять при автоматизации подготовки и зачистки ресурсов
'''
class DatabaseConnection:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def __enter__(self):
        print(f"[БАЗА] Подключаюсь к {self.db_name}...")
        return self  # Этот объект запишется в переменную после слова 'as'

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("[БАЗА] Закрываю соединение и освобождаю память.")
        # Если внутри with произошла ошибка, данные о ней придут в аргументы.
        # Возврат False (или ничего) заставит ошибку лететь дальше.
        return False

# Использование кастомного менеджера:
with DatabaseConnection("production.db") as db:
    print("[КОД] Выполняю SQL-запросы...")
