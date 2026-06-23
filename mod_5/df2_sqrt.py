'''
как создать функцию
'''
target = 2013  # глобальные
x = 1
while True:
    oldx = x
    x = (x+target/x)/2
    if (oldx == x):
        break

print(x)

def my_sqrt(target):
    x = 1 # локальные
    while True:
        oldx = x
        x = (x+target/x)/2
        if (oldx == x):
            break
    return x

y = 2013
r = my_sqrt(y)
od = my_sqrt
rr = od(y)
print(r, rr, od, my_sqrt)
