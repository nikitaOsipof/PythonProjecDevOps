s = 'ab12c59p7dq'
digits = []
for symbol in s:
    if '1234567890'.find(symbol) != -1:
        digits.append(int(symbol))
print(digits)
print(s)

ds = [int(x) for x in s if '1234567890'.find(x) != -1]
dsg = (int(x) for x in s if '1234567890'.find(x) != -1)
print(f"List {ds} Geg {dsg}")

for val in dsg:
    print('Gen еще раз', val)