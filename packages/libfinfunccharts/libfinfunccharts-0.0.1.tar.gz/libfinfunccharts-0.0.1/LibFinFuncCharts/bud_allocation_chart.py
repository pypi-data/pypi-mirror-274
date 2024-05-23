def budallocation_chart():
    # импорт нужных модулей
    import matplotlib.pyplot as plt 
    import numpy as np 

    # спрашиваем у пользователя, что вводить: расходы или доходы
    name_of_exp_or_inc = str(input("Расходы или доходы (все буквы строчные)? "))
    if name_of_exp_or_inc == "расходы":
        # вводим, сколько денег уходит на каждый расход (в руб.)
        elnt_1 = float(input("Сколько руб. уходит на 1-й расход: ")) 
        elnt_2 = float(input("Сколько руб. уходит на 2-й расход: "))
        elnt_3 = float(input("Сколько руб. уходит на 3-й расход: "))
        elnt_4 = float(input("Сколько руб. уходит на 4-й расход: "))
        elnt_5 = float(input("Сколько руб. уходит на 5-й расход: "))
        elnt_6 = float(input("Сколько руб. уходит на 6-й расход: "))
        elnt_7 = float(input("Сколько руб. уходит на 7-й расход: "))
        elnt_8 = float(input("Сколько руб. уходит на 8-й расход: "))
        elnt_9 = float(input("Сколько руб. уходит на 9-й расход: "))
        elnt_10 = float(input("Сколько руб. уходит на 10-й расход: "))

        # сумма всех расходов
        summ_elnt = elnt_2 + elnt_2 + elnt_3 + elnt_4 + elnt_5 + elnt_6 + elnt_7 + elnt_8 + elnt_9 + elnt_10 

        # находим, сколько процентов составляет каждый расход от всех расходов
        elnt_1_percent = elnt_1 / summ_elnt 
        elnt_2_percent = elnt_2 / summ_elnt
        elnt_3_percent = elnt_3 / summ_elnt 
        elnt_4_percent = elnt_4 / summ_elnt 
        elnt_5_percent = elnt_5 / summ_elnt 
        elnt_6_percent = elnt_6 / summ_elnt 
        elnt_7_percent = elnt_7 / summ_elnt
        elnt_8_percent = elnt_8 / summ_elnt
        elnt_9_percent = elnt_9 / summ_elnt 
        elnt_10_percent = elnt_10 / summ_elnt   

        # указываем название каждого расхода
        elnt_1_name = input(f"Введите название 1-ого расхода: ")
        elnt_2_name = input(f"Введите название 2-ого расхода: ")
        elnt_3_name = input(f"Введите название 3-его расхода: ")
        elnt_4_name = input(f"Введите название 4-ого расхода: ")
        elnt_5_name = input(f"Введите название 5-ого расхода: ")
        elnt_6_name = input(f"Введите название 6-ого расхода: ")
        elnt_7_name = input(f"Введите название 7-ого расхода: ")
        elnt_8_name = input(f"Введите название 8-ого расхода: ")
        elnt_9_name = input(f"Введите название 9-ого расхода: ")
        elnt_10_name = input(f"Введите название 10-ого расхода: ")

        # список процентов
        list_of_percent = [elnt_1_percent, elnt_2_percent, elnt_3_percent, elnt_4_percent, elnt_5_percent, elnt_6_percent, elnt_7_percent, elnt_8_percent, elnt_9_percent, elnt_10_percent]

        # список названий расходов
        list_of_name = [elnt_1_name, elnt_2_name, elnt_3_name, elnt_4_name, elnt_5_name, elnt_6_name, elnt_7_name, elnt_8_name, elnt_9_name, elnt_10_name]

        fig = plt.figure(figsize =(10, 10)) # размер диаграммы
        plt.pie(list_of_percent, labels=list_of_name, autopct="%1.1f%%") # параметры диаграммы
        plt.title("Круговая диаграмма расходов\n") # заголовок диаграммы
        plt.show() # показ диаграммы
    

    elif name_of_exp_or_inc == "доходы":
        
        # вводим, сколько денег составляет каждый доход (в руб.)
        elnt_1 = float(input("Сколько руб. составляет 1-й доход: ")) 
        elnt_2 = float(input("Сколько руб. составляет 2-й доход: "))
        elnt_3 = float(input("Сколько руб. составляет 3-й доход: "))
        elnt_4 = float(input("Сколько руб. составляет 4-й доход: "))
        elnt_5 = float(input("Сколько руб. составляет 5-й доход: "))
        elnt_6 = float(input("Сколько руб. составляет 6-й доход: "))
        elnt_7 = float(input("Сколько руб. составляет 7-й доход: "))
        elnt_8 = float(input("Сколько руб. составляет 8-й доход: "))
        elnt_9 = float(input("Сколько руб. составляет 9-й доход: "))
        elnt_10 = float(input("Сколько руб. составляет 10-й доход: "))

        # сумма всех доходов
        summ_elnt = elnt_2 + elnt_2 + elnt_3 + elnt_4 + elnt_5 + elnt_6 + elnt_7 + elnt_8 + elnt_9 + elnt_10 

        # находим, сколько процентов составляет каждый доход от всех доходов
        elnt_1_percent = elnt_1 / summ_elnt 
        elnt_2_percent = elnt_2 / summ_elnt
        elnt_3_percent = elnt_3 / summ_elnt 
        elnt_4_percent = elnt_4 / summ_elnt 
        elnt_5_percent = elnt_5 / summ_elnt 
        elnt_6_percent = elnt_6 / summ_elnt 
        elnt_7_percent = elnt_7 / summ_elnt
        elnt_8_percent = elnt_8 / summ_elnt
        elnt_9_percent = elnt_9 / summ_elnt 
        elnt_10_percent = elnt_10 / summ_elnt   

        # указываем название каждого дохода
        elnt_1_name = input(f"Введите название 1-ого дохода: ")
        elnt_2_name = input(f"Введите название 2-ого дохода: ")
        elnt_3_name = input(f"Введите название 3-его дохода: ")
        elnt_4_name = input(f"Введите название 4-ого дохода: ")
        elnt_5_name = input(f"Введите название 5-ого дохода: ")
        elnt_6_name = input(f"Введите название 6-ого дохода: ")
        elnt_7_name = input(f"Введите название 7-ого дохода: ")
        elnt_8_name = input(f"Введите название 8-ого дохода: ")
        elnt_9_name = input(f"Введите название 9-ого дохода: ")
        elnt_10_name = input(f"Введите название 10-ого дохода: ")

        # список процентов
        list_of_percent = [elnt_1_percent, elnt_2_percent, elnt_3_percent, elnt_4_percent, elnt_5_percent, elnt_6_percent, elnt_7_percent, elnt_8_percent, elnt_9_percent, elnt_10_percent]

        # список названий доходов
        list_of_name = [elnt_1_name, elnt_2_name, elnt_3_name, elnt_4_name, elnt_5_name, elnt_6_name, elnt_7_name, elnt_8_name, elnt_9_name, elnt_10_name]

        fig = plt.figure(figsize =(10, 10)) # размер диаграммы
        plt.pie(list_of_percent, labels=list_of_name, autopct="%1.1f%%") 
        plt.title("Круговая диаграмма доходов\n")
        plt.show() # показ диаграммы