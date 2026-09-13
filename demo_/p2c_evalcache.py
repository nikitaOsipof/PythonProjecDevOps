import evalcache
# \DemoUV\de-modern-setup>uv add evalcache
# Настраиваем хранилище кэша на диске
hd_cache = evalcache.DirCache(".cache_directory")
lazy = evalcache.Lazy(hd_cache)

@lazy
def heavy_computation(x, y):
    print("Выполняю тяжелую математику...")  # Напечатается ОДИН раз за все запуски scripts
    return x ** y + 42

# 1. Никаких вычислений не происходит. heavy_computation НЕ вызывается.
# Вместо этого в `res` записывается "ленивый объект" с просчитанным хэшем.
res = heavy_computation(10, 5)

# 2. А вот теперь магия:
print(res.unlazy())  # Первый запуск: функция выполнится, результат сохранится на диск.
print(res.unlazy())  # Второй запуск: функция проигнорируется, результат мгновенно сочтется с диска!
