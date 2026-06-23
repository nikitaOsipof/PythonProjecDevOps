'''
Что принимают функции и что они возвращают
'''
s = sum([1,2])
print("sum:", s, "dqwe", sep=';')  # *values  sep - именованный параметр

print(all([True, True, 10, 0]))
print((any([False, 0, 1])))

pas = "qwqeer123"
check = [
    len(pas) > 8,
    any(char.isdigit() for char in pas)
]

if all(check):
    print("ok")
else:
    print('bad')
# контрольное упражнение = сделать функцией как часть pipeline
