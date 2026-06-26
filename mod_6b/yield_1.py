# В обоих случаях результат вызова функции будет одинаковым, но yield from делает код лаконичнее.

def get_ips_yield():
    subnets = [["192.168.1.1", "192.168.1.2"], ["10.0.0.1", "10.0.0.2"]]
    for subnet in subnets:
        for ip in subnet:
            yield ip  # Возвращаем каждый IP по одному


def get_ips_yield_from():
    subnets = [["192.168.1.1", "192.168.1.2"], ["10.0.0.1", "10.0.0.2"]]
    for subnet in subnets:
        yield from subnet  # Автоматически выдает все элементы из subnet

get_ips_yield()
get_ips_yield_from()