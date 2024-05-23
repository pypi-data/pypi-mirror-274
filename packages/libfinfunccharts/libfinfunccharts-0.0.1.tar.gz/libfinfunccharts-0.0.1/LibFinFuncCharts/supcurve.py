def sup_curve():
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots()
    plt.title("Кривая предложения") # заголовок графика
    plt.xlabel('Q, количество товаров') # ось Q
    plt.ylabel('P, цена товара') # ось P
    a = float(input("Введите коэффициент a: ")) # a — коэффициент, задающий смещение начала линии по оси Q
    b = float(input("Введите коэффициент d (d > 0): ")) # d — коэффициент, задающий угол наклона линии (d > 0)
    if b > 0:
        Q = float(input("Введите количество товаров: ")) # количество товара
        Q =  np.linspace(0, 10, 100) # Q от 0 до 10, разбитое на 100 равных точек
        P = a+b*Q # функция предложения
        # показ графика
        plt.plot(P, Q) 
        plt.show() 
    else:
        print("Ошибка! Введите b, большее нуля: ")