'''
Функция вычисляет среднее продолжающегося ряда чисел, например среднюю цену закрытия биржевого товара за всю историю торгов.
 Каждый день ряд пополняется новой ценой, а при вычислении среднего учитываются все прежние цены.
'''
def  make_averager():
    '''
    При обращении к make_averager возвращается объект-функция averager.
    При каждом вызове averager добавляет переданный аргумент в конец списка series и вычисляет текущее среднее
    '''
    series = []
    def averager(new_value):
        series.append(new_value)
        total  =  sum(series)
        return total / len(series)
    return  averager

avg  =  make_averager()
print(avg(10))                 # 10.0
print(avg(11))                 # 10.5
print(avg(15))                 # 12.0

print(avg.__code__.co_varnames)  # ('new_value', 'total')
print(avg.__code__.co_freevars)  # ('series',)
print(avg.__closure__[0].cell_contents) # [10, 11, 15]