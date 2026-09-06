numbers = [2, 3, 5, 7, 11, 13, 2, 17, 19, 2, 12, 3, 3, 3]
numbers.remove(2)
print(numbers)

while 2 in numbers:
    numbers.remove(2)

print(numbers)

numbers = [num for num in numbers if num !=3]
print(numbers)
