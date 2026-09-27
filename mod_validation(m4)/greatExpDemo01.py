import great_expectations as gx
import pandas as pd

# 1. Подготовка данных из вашего примера
df = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "price": [100, 250, -10, 500],
    "status": ["ordered", "shipped", "deleted", "delivered"]
})

# 2. Инициализация контекста (создаст инфраструктуру GX)
context = gx.get_context()

# 3. Регистрация данных (Data Source -> Asset -> Batch Definition)
# Это стандартный путь в GX 1.x для работы с Pandas
ds = context.data_sources.add_pandas(name="retail_source")
asset = ds.add_dataframe_asset(name="orders_asset")
batch_def = asset.add_batch_definition_whole_dataframe(name="batch_all")

# 4. Создание набора правил (Expectation Suite)
suite = context.suites.add(gx.ExpectationSuite(name="retail_quality_suite"))

# Добавляем ваши правила из примера:
# Правило 1: Уникальность ID
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="id"))

# Правило 2: Цена >= 0
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="price", min_value=0))

# Правило 3: Статусы только из списка (здесь 'deleted' вызовет ошибку)
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(
    column="status",
    value_set=["ordered", "shipped", "delivered"]
))

# 5. Связываем данные и правила (Validation Definition)
validation_def = context.validation_definitions.add(
    gx.ValidationDefinition(
        name="retail_validation",
        data=batch_def,
        suite=suite
    )
)

# 6. Настройка Checkpoint (запуск + генерация отчета)
checkpoint = context.checkpoints.add(
    gx.Checkpoint(
        name="retail_checkpoint",
        validation_definitions=[validation_def],
        actions=[gx.checkpoint.UpdateDataDocsAction(name="update_docs")] # Обновляет HTML
    )
)

# 7. Запуск! Передаем наш DataFrame
result = checkpoint.run(batch_parameters={"dataframe": df})

# 8. Финал: открываем визуальный отчет в браузере
context.build_data_docs()
context.open_data_docs()

print(f"Общий статус валидации: {'✅ Успех' if result.success else '❌ Провал'}")
