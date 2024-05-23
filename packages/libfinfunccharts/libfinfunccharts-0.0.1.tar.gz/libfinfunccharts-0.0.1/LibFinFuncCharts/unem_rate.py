def unemrate():
    numb_of_unem = float(input()) # число безработных
    work_size = float(input()) # численность рабочей силы
    un_rate = numb_of_unem / work_size * 100 # уровень безработицы
    print(f"Уровень безработицы: {un_rate}")   
