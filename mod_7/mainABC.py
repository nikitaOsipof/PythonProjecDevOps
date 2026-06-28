from infrastructure.nodesABC import WebAgent, BaseAgent

if __name__ == "__main__":
    print("--- Попытка создать абстрактный класс ---")
    try:
        # Это должно упасть с ошибкой, так как BaseAgent абстрактный!
        agent = BaseAgent("Generic")
    except TypeError as e:
        print(f"❌ Как и ожидалось, ошибка: {e}")

    print("\n--- Работа с конкретным Агентом ---")
    web_check = WebAgent(name="GitHub_Status", target_url="https://github.com")

    # Выполняем проверку
    web_check.execute_check()
    print(f"Статус агента после проверки: {web_check.status}")

    # Используем метод, подмешанный из Миксина
    web_check.save_to_json("agent_report.json")
