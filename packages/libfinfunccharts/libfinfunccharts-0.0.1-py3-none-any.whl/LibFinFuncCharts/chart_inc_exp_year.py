def chartinc_exp_year():
    # импортируем нужные библиотеки
    import matplotlib.pyplot as plt
    import numpy as np

    width = 0.4 # ширина
    abscissa_list = list(range(0,12)) # сколько элементов поместится в список

    # вводим, сколько денег составляют доходы за каждый месяц 
    income_1 = float(input("Сколько денег составляют доходы за январь: "))
    income_2 = float(input("Сколько денег составляют доходы за февраль: "))
    income_3 = float(input("Сколько денег составляют доходы за март: "))
    income_4 = float(input("Сколько денег составляют доходы за апрель: "))
    income_5 = float(input("Сколько денег составляют доходы за май: "))
    income_6 = float(input("Сколько денег составляют доходы за июнь: "))
    income_7 = float(input("Сколько денег составляют доходы за июль: "))
    income_8 = float(input("Сколько денег составляют доходы за август: "))
    income_9 = float(input("Сколько денег составляют доходы за сентябрь: "))
    income_10 = float(input("Сколько денег составляют доходы за октябрь: "))
    income_11 = float(input("Сколько денег составляют доходы за ноябрь: "))
    income_12 = float(input("Сколько денег составляют доходы за декабрь: "))

    # список доходов
    income_list = [income_1, income_2, income_3, income_4, income_5, income_6, income_7, income_8, income_9, income_10, income_11, income_12]

    # вводим, сколько денег уходит на расходы за каждый месяц 
    expenses_1 = float(input("Сколько денег уходит на расходы за январь: "))
    expenses_2 = float(input("Сколько денег уходит на расходы за февраль: "))
    expenses_3 = float(input("Сколько денег уходит на расходы за март: "))
    expenses_4 = float(input("Сколько денег уходит на расходы за апрель: "))
    expenses_5 = float(input("Сколько денег уходит на расходы за май: "))
    expenses_6 = float(input("Сколько денег уходит на расходы за июнь: "))
    expenses_7 = float(input("Сколько денег уходит на расходы за июль: "))
    expenses_8 = float(input("Сколько денег уходит на расходы за август: "))
    expenses_9 = float(input("Сколько денег уходит на расходы за сентябрь: "))
    expenses_10 = float(input("Сколько денег уходит на расходы за октябрь: "))
    expenses_11 = float(input("Сколько денег уходит на расходы за ноябрь: "))
    expenses_12 = float(input("Сколько денег уходит на расходы за декабрь: "))

    # список расходов
    expenses_list = [expenses_1, expenses_2, expenses_3, expenses_4, expenses_5, expenses_6, expenses_7, expenses_8, expenses_9, expenses_10, expenses_11, expenses_12]

    # индексы столбиков на оси абсцисс
    abscissa_index = np.arange(len(abscissa_list))

    plt.title("Столбчатая диаграмма, показывающая динамику изменения доходов и расходов в течение года") # название диаграммы
    plt.xlabel("Месяцы") # название оси абсцисс

    # названия индексов столбиков на оси абсцисс
    plt.xticks(abscissa_index, ["Январь", "Февраль", "Март","Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]) 
    plt.ylabel("Количество денег, руб.") # название оси ординат

    # расположение столбиков
    plt.bar(abscissa_index - (width / 2), income_list, label="Доходы", width=width)
    plt.bar(abscissa_index + (width / 2), expenses_list, label="Расходы", width=width)
    plt.legend() # легенда
    plt.show() # показ графика