import itertools

def lazy_id_generator():
    # Бесконечные ленивые счетчики
    ids = itertools.count(start=1)
    # Чередуем роли пользователей по кругу
    roles = itertools.cycle(['User', 'Admin', 'Moderator'])

    while True:
        # zip берет по одному элементу из каждого ленивого источника
        current_id = next(ids)
        current_role = next(roles)
        yield f"ID: {current_id:04d} | Role: {current_role}"


# Создаем генератор (он ленив, ничего пока не считает)
gen = lazy_id_generator()

# Берем первые 4 элемента
for _ in range(4):
    print(next(gen))


# Выведет:
# ID: 0001 | Role: User
# ID: 0002 | Role: Admin
# ID: 0003 | Role: Moderator
# ID: 0004 | Role: User
