def mini_pipeline():
    print("[LOG] Начат этап А")
    yield "Первый отчет"
    
    print("[LOG] Начат этап Б")
    yield "Второй отчет"
    
    print("[LOG] Начат этап В")
    yield "Финальный отчет"

# 1. Просто создаем генератор. Код функции ЕЩЕ НЕ НАЧАЛ выполняться!
# В консоли сейчас пусто. Память = 0.
generator = mini_pipeline() 

print("--- Нажимаем кнопку next() в первый раз ---")
res1 = next(generator) 
print(f"Получили из потока: {res1}\n")

print("--- Нажимаем кнопку next() во второй раз ---")
res2 = next(generator)
print(f"Получили из потока: {res2}\n")

print("--- Нажимаем кнопку next() в третий раз ---")
res3 = next(generator)
print(f"Получили из потока: {res3}\n")

print("--- Четвертый нажим (Данные кончились) ---")
try:
    next(generator)
except StopIteration:
    print("[StopIteration] Поток пуст! Конвейер официально остановился.")
