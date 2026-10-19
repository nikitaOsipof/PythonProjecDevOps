from datetime import datetime, timedelta
# Имитируем импорты Airflow, чтобы показать студентам структуру декларации графа
try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
except ImportError:
    # Заглушка, если код запускается локально без Airflow
    class DAG: pass
    class PythonOperator: pass

# Вспомогательные функции-шаги автоматизации контента
def check_plagiarism():
    print("[Шаг 1] Текст проверен на уникальность: 98%.")

def generate_ai_cover():
    print("[Шаг 2] Нейросеть сгенерировала обложку для статьи.")

def publish_to_website():
    print("[Шаг 3] Статья успешно опубликована на веб-портале.")

# Описание метаданных и расписания автоматизации
default_args = {
    'owner': 'content_manager',
    'start_date': datetime(2026, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

# Декларация графа (DAG)
with DAG(
    dag_id='blog_publication_workflow',
    default_args=default_args,
    schedule_interval='@weekly', # Запуск раз в неделю
    catchup=False
) as dag:

    # Объявление задач (Tasks)
    task_validate = PythonOperator(
        task_id='check_text_plagiarism',
        python_callable=check_plagiarism
    )

    task_image = PythonOperator(
        task_id='generate_cover_via_ai',
        python_callable=generate_ai_cover
    )

    task_publish = PythonOperator(
        task_id='post_to_wordpress',
        python_callable=publish_to_website
    )

    # 🔀 Объяснение концепции битовых сдвигов (Граф зависимостей)
    # Задачи проверки текста и генерации обложки могут идти параллельно,
    # но публикация начнется ТОЛЬКО тогда, когда оба предыдущих шага успешны.
    [task_validate, task_image] >> task_publish
