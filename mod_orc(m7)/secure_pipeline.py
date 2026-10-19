from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook


@dag(
    dag_id='idempotent_postgresql_pipeline_2026',
    schedule='@daily',
    start_date=datetime(2026, 10, 1),
    catchup=False,
    tags=['architecture', 'idempotency']
)
def my_secure_pipeline():
    @task()
    def extract_and_load_data(**context):
        # 1. Получаем СТРОГУЮ дату, за которую должен работать этот запуск
        # Airflow передает ее в контекст. Формат: YYYY-MM-DD
        target_date = context['data_interval_start'].strftime('%Y-%m-%d')
        print(f"Начало обработки данных за бизнес-день: {target_date}")

        # Имитируем получение данных из источника за эту дату
        # (в реальности тут был бы запрос к API или другой БД)
        mock_api_data = [
            {"order_id": 101, "amount": 250.50, "date": target_date},
            {"order_id": 102, "amount": 1400.00, "date": target_date}
        ]

        # 2. Инициализируем подключение к нашей базе данных (через Connection в Airflow)
        pg_hook = PostgresHook(postgres_conn_id='my_postgres_db')

        # Получаем стандартный курсор для транзакций
        with pg_hook.get_conn() as conn:
            with conn.cursor() as cursor:
                # ШАГ 1 ДЛЯ ИДЕМПОТЕНТНОСТИ: Очищаем старые данные за этот день,
                # если они там были (например, от прошлой упавшей попытки)
                delete_query = "DELETE FROM daily_sales WHERE order_date = %s;"
                cursor.execute(delete_query, (target_date,))
                print(f"Старые данные за {target_date} успешно удалены (если существовали).")

                # ШАГ 2 ДЛЯ ИДЕМПОТЕНТНОСТИ: Безопасно вставляем новые данные
                insert_query = """
                    INSERT INTO daily_sales (order_id, amount, order_date) 
                    VALUES (%s, %s, %s);
                """
                for record in mock_api_data:
                    cursor.execute(insert_query, (record['order_id'], record['amount'], record['date']))

                # Фиксируем транзакцию. Если код упадет ДО этой строчки,
                # база данных автоматически откатит (Rollback) все изменения!
                conn.commit()

        print(f"Данные за {target_date} успешно и безопасно записаны.")

    # Вызов задачи
    extract_and_load_data()


my_secure_pipeline()
