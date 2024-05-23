def forecastsales_year():
    # импортируем библиотеку matplotlib
    import matplotlib.pyplot as plt 

    # вводим значения 
    month_sales_1 = float(input("Кол-во проданных товаров за январь: "))
    month_sales_2 = float(input("Кол-во проданных товаров за февраль: "))
    month_sales_3 = float(input("Кол-во проданных товаров за март: "))
    month_sales_4 = float(input("Кол-во проданных товаров за апрель: "))
    month_sales_5 = float(input("Кол-во проданных товаров за май: "))
    month_sales_6 = float(input("Кол-во проданных товаров за июнь: "))
    month_sales_7 = float(input("Кол-во проданных товаров за июль: "))
    month_sales_8 = float(input("Кол-во проданных товаров за август: "))
    month_sales_9 = float(input("Кол-во проданных товаров за сентябрь: "))
    month_sales_10 = float(input("Кол-во проданных товаров за октябрь: "))
    month_sales_11= float(input("Кол-во проданных товаров за ноябрь: "))
    month_sales_12 = float(input("Кол-во проданных товаров за декабрь: "))

    # список проданных товаров
    sales_list = [month_sales_1, month_sales_2, month_sales_3, month_sales_4, month_sales_5, month_sales_6, month_sales_7, month_sales_8, month_sales_9, month_sales_10, month_sales_11, month_sales_12]
    price_product = float(input("Введи цену товара: ")) # цена

    # прогноз продаж (расчёт)
    sales_forecast = [sale * price_product for sale in sales_list]

    # навзание месяцев на оси абсцисс
    months_index = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    for month_number in range(1, 13):
        print(f"{month_number} - {months_index[month_number-1]}")
    plt.plot(months_index, sales_forecast, marker = '^') # пересечение коордиант
    plt.title("Прогноз продаж в течение года") # название графика
    plt.xlabel("Месяцы") # название оси абсцисс
    plt.ylabel("Кол-во проданных товаров") # название оси ординат
    plt.xticks(months_index) # расположение месяцев на оси абсцисс
    plt.grid(True)
    plt.show() # показ графика