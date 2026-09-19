'''
Если внутри замыкания (например, в декораторах мониторинга) нужно не просто прочитать переменную из внешнего контекста,
а изменить её, например, посчитать количество, то если просто написать counter += 1, Python решит, что вы хотите создать
новую локальную переменную, и выдаст ошибку.
Чтобы сказать Python «измени переменную во внешней функции», используется nonlocal
'''

def out(str):
    count = len(str)
    print(count)
    def nestout():
        count = len(str) # приходится повторно вычислять количество
        count +=1
        print(str, count)
    nestout()

out("dfcz")

def out(str):
    count = len(str)
    print(count)
    def nestout():
        nonlocal count
        #count = len(str) # можно повторно не вычислять количество
        count +=1
        print(str, count)
    nestout()

out("dfcz")


