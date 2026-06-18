dM = ("qwerT", (10,100), [12,35,], True)
dMdist = {'model':"qweT",
          'var':(10, 100),
          'data':[12.35],
          'F':True}
print(type(dMdist))
print(dMdist)
'''
numbers = [1, 2, 3]
letters = ['a', 'b', 'c']
zipped = zip(numbers, letters)
print(zipped) # iterator object - <zip object at 0x7fa4831153c8>
print(type(zipped))     # <class 'zip'>
print(list(zipped))     # [(1, 'a'), (2, 'b'), (3, 'c')] --- элементы имеют строгий порядок
'''
print(dMdist['var'])
dMdist['data'].append(123)
print(dMdist)

s2 = set([11, 2,3, 33, 4, 5, 2, 11, 33,45, 3]) # применяет функцию set(), передав в качестве аргумента любой итерируемый объект.
print(s2)
'''
Пример 1
Есть наборы данных:
haystack содержит уникальные данные адресов
needles - особые важные адреса
Задача: подсчитать, сколько раз элементы needles встречаются в haystack. 
Рекомендуется применить операцию пересечения множеств (оператор &)
'''
haystack = {12, 34, 45, 23, 1, 5, 9, 54, 3}
needles = {1, 5, 3, 22, 32}
found = len(needles & haystack)
print(found)

''' для любых итерируемых типов'''
haystack = [12, 34, 45, 23, 1, 5, 9, 54, 3]  # список
needles = (1, 5, 3, 22, 32)  # кортеж
found = len(set(needles) & set(haystack))
print(found)
