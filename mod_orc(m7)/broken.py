# Пример DAG с циклом, который вызовет ошибку при парсинге в Airflow
# (Этот код предназначен для демонстрации ошибки, его нельзя сохранять в папку dags/)

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def task_a():
    print("Выполняю задачу A")


def task_b():
    print("Выполняю задачу B")


def task_c():
    print("Выполняю задачу C")


with DAG(
        dag_id="broken_cycle_dag",
        start_date=datetime(2025, 1, 1),
        schedule=None,
        catchup=False,
) as dag:
    t1 = PythonOperator(
        task_id="task_a",
        python_callable=task_a
    )

    t2 = PythonOperator(
        task_id="task_b",
        python_callable=task_b
    )

    t3 = PythonOperator(
        task_id="task_c",
        python_callable=task_c
    )

    # Создаем цикл зависимостей: A -> B -> C -> A
    t1 >> t2
    t2 >> t3
    t3 >> t1  # Эта строка замыкает цикл

# Если попытаться загрузить этот файл, Airflow выбросит исключение:
# airflow.exceptions.AirflowDagCycleException: Cycle detected in DAG 'broken_cycle_dag'."""
#Решение
# Было (цикл):
# t1 >> t2
# t2 >> t3
# t3 >> t1

# Стало (корректный DAG):
t1 >> t2
t2 >> t3
# Зависимость t3 >> t1 удалена. Теперь граф линеен: A -> B -> C.