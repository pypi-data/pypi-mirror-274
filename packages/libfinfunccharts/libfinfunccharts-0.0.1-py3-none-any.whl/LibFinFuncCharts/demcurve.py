def dem_curve():
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots()
    plt.title('Кривая спроса') # заголовок графика
    plt.xlabel('Q, количество товаров') # ось Q
    plt.ylabel('P, цена товара') # ось P
    a = float(input("Введите коэффициент a: ")) # a — коэффициент, задающий смещение начала линии по оси Q
    b = float(input("Введите коэффициент b (b < 0): ")) # b — коэффициент задающий угол наклона линии (b < 0)
    if b < 0:
        Q = float(input("Введите количество товаров: ")) # количество товара
        Q = np.linspace(0, 10, 100) # Q от 0 до 10 разбитое на 100 равных точек
        P = a + b*Q # функция спроса
        # показ графика
        plt.plot(Q, P)  
        plt.show()
    else:
        print("Ошибка! Введите b, меньшее нуля: ")
