def  make_averager():
    count = 0
    total =  0.0

    def  averager(new_value: float) -> float:
        nonlocal   count,   total
        count += 1
        total += new_value
        return total / count
    return  averager


avg  =  make_averager()
print(avg(10))                 # 10.0
print(avg(11))                 # 10.5
print(avg(15))                 # 12.0

print(avg.__code__.co_varnames)  # ('new_value',)
print(avg.__code__.co_freevars)  # ('count', 'total')

print(avg.__closure__)  # (<cell at 0x0000023C69B343A0: int object at 0x00007FFB9EC449F8>, <cell at 0x0000023C69B34370: float object at 0x0000023C6989AC90>)
print(avg.__closure__[0].cell_contents) # 3