# Library with financial functions and charts #

## Что это такое? ##
Это библиотека, состоящая из различных функций для финансовых расчётов и построения графиков, а также диаграмм.


----------


## Как пользоваться? ##


Для начала нужно импортировать библиотеку: 

    import libfinfunccharts

Можно использовать сокращённое имя библиотеки:

    import libfinfunccharts as lffc

Либо же импортировать определённые функции:

    from libfinfunccharts import unemrate


----------


## Функции ##


Рассмотрим несколько функций.
1. `unemrate()` - функция, которая определяет уровень безработицы. Сначала вводим число безработных, потом численность рабочей силы и получаем результат. 
Её код:

```python
numb_of_unem = float(input()) # число безработных
work_size = float(input()) # численность рабочей силы
un_rate = numb_of_unem / work_size * 100 # уровень безработицы
print(f"Уровень безработицы: {un_rate}")
``` 

2. `employrate()` - функция, опредеяющая уровень занятости. Здесь вводим значения. Какие именно, указано в структуре.
Код:  

```python    
numb_of_emp = float(input()) # число занятых
work_size = float(input()) # численность рабочей силы
emp_rate = numb_of_emp / work_size * 100 # уровень занятости
print(f"Уровень занятости: {emp_rate}")
```

3. `volsurplus()` - функция, считающая объём излишек.
Код:

```python
Q_prop = float(input()) # величина предложения
Q_dem = float(input()) # величина спроса
vol_sur = Q_prop - Q_dem # объём излишек
print(f"Объём излишек: {vol_sur}")
```
 
4. `voldeficit()` - функция, считающая объём дефецита.
Код:

```python
Q_dem = float(input()) # величина спроса
Q_prop = float(input()) # величина предложения
vol_def = Q_dem - Q_prop # объём дефецита
print(f"Объём дефицита: {vol_def}")
```

5. `simpleinter()` - функция простого процента.
Код:

```python
P_debt = float(input()) # сумма долга с процентами
n_days = float(input()) # количество дней
ann_inter = float(input()) # годовой процент в долях
C_credit = P_debt * (1 + ann_inter * n_days / 360) # общая сумма кредита
print(f"Простой процент: {C_credit}")
```

6. `selrevenue ()` - функция, высчитывающая выручки продавца.
Код:

```python
P_price = float(input()) # цена
Q_quan = float(input()) # количество
T_seller = P_price * Q_quan # выручка продавца
print(f"Выручка продавца: {T_seller}")
```

7. `realincome()` - функция, считающая реальный доход.
Код:

```python
nom_inc = float(input()) # номинальный доход
con_price_ind = float(input()) # показатель индекса потребительских цен
real_inc = nom_inc / con_price_ind * 100 # реальный доход
print(f"Реальный доход: {real_inc}")
```

8. `profitcal()` - функция расчёта прибыли. 
Код:

```python
T_seller = float(input()) # совокупный доход (выручка продавца)
T_costs = float(input()) # общие затраты
P_profit = T_seller - T_costs # расчёт прибыли  
print(f"Расчёт прибыли: {P_profit}")
```

9. `avefixed_costs()` - функция расчёта средних постоянных издержек. 
Код:

```python
fix_costs = float(input()) # постоянные издержки
prod_vol = float(input()) # объём производства
ave_fix_costs = fix_costs / prod_vol # средние постоянные издержки
print(f"Средние постоянные издержки: {ave_fix_costs}")
```

10. `avetotal_costs()` - функция, расчитывающая средние общие издержки.
Код:

```python
tot_costs = float(input()) # общие издержки
prod_vol = float(input()) # объём производства
ave_tot_costs = tot_costs / prod_vol # средние общие издержки
print(f"Средние общие издержки: {ave_tot_costs}")
```

11. `avevariable_costs()` - функция, расчитывающая средние переменные издержки.
Код:

```python
variable_costs = float(input())
prod_vol = float(input()) # объём производства
ave_var_costs = variable_costs / prod_vol # средние переменные издержки
print(f"Средние переменные издержки: {ave_var_costs}")
```

12. `calad_1_cur_assets_1()` - функция, расчитывающая среднюю продолжительность одного оборота оборотных активов в днях (1-й способ).
Код:

```python
ave_bal_of_cur_assets_for_the_period = float(input()) # средние остатки оборотных активов за период
numb_days_in_period = float(input()) # число дней в периоде (в месяце — 30, в квартале — 90, в году — 360)
revenue = float(input()) # выручка
ad_of_1_turn_of_cur_assets = (ave_bal_of_cur_assets_for_the_period*numb_days_in_period)/revenue # сред. про-сть 1-ого оборота об-ных активов
print(f"Cредняя продолжительность одного оборота оборотных активов (в днях): {ad_of_1_turn_of_cur_assets}")
```

13. `calad_1_cur_asset_2()` - та же функция, но считает по 2-му способу.
Код:

```python
ave_bal_of_cur_assets_for_the_period = float(input()) # средние остатки оборотных активов за период
ave_daily_renuvue = float(input()) # среднедневная выручка
ad_of_1_turn_of_cur_assets = ave_bal_of_cur_assets_for_the_period / ave_daily_renuvue # сред. про-сть 1-ого оборота об-ных активов
print(f"Cредняя продолжительность одного оборота оборотных активов (в днях): {ad_of_1_turn_of_cur_assets}")
```

14. `calinv_turn_days()` - функция, определяющая оборачиваемость запасов в днях.
Код:

```python
ave_stock_bal_period = float(input()) # средние остатки запасов за период
cost_of_sales = float(input()) # себестоимость продаж
numb_days_in_period = float(input()) # число дней в периоде (в месяце — 30, в квартале — 90, в году — 360)
inv_turn_in_days = ave_stock_bal_period * numb_days_in_period / cost_of_sales # оборачиваемость запасов в днях
print(f"Оборачиваемость запасов в днях: {inv_turn_in_days}")
```

15. `calinv_turn_times()` - функция, определяющая оборачиваемость запасов в разах.
Код:

```python
cost_of_sales = float(input()) # себестоимость продаж
ave_stock_bal_period = float(input()) # средние остатки запасов за период
inv_turn_in_times = cost_of_sales / ave_stock_bal_period # оборачиваемость запасов в разах
print(f"Оборачиваемость запасов в разах: {inv_turn_in_times}")
```

16. `calowm_work_cap_1()` - функция расчёта собственного оборотного капитала (1-й способ).
Код:

```python
own_cap = float(input()) # собственный капитал
ns_assets = float(input()) # внеоборотные активы
owm_work_cap = own_cap - ns_assets # собственный оборотный капитал
print(f"Собственный оборотный капитал: {owm_work_cap}")
```

17. `calowm_work_cap_2()` - та же функция, но расчитывающая по 2-му способу.
Код:

```python
own_cap = float(input()) # собственный капитал
lt_obligations = float(input()) # долгосрочные обязательства
ns_assets = float(input()) # внеоборотные активы
owm_work_cap = own_cap + lt_obligations - ns_assets  # собственный оборотный капитал
print(f"Собственный оборотный капитал: {owm_work_cap}")
``` 

18. `calturn_days()` - функция, определяющая оборачиваемость в днях.
Код:

```python
revenue = float(input()) # выручка
ave_cash_and_CEB_period = float(input()) # средние остатки денежных средств и денежных эквивалентов за период
ave_bal_of_STFI_period = float(input()) # средние остатки краткосрочных финансовых вложений за период
numb_days_in_period = float(input()) # число дней в периоде (в месяце — 30, в квартале — 90, в году — 360)
turn_in_days = (ave_cash_and_CEB_period + ave_bal_of_STFI_period) * numb_days_in_period / revenue # оборачиваемость в днях
print(f"Оборачиваемость в днях: {turn_in_days}")
```

19. `calturn_times()` - функция, определяющая оборачиваемость в разах.
Код:

```python
revenue = float(input()) # выручка
ave_cash_and_CEB_period = float(input()) # средние остатки денежных средств и денежных эквивалентов за период
ave_bal_of_STFI_period = float(input()) # средние остатки краткосрочных финансовых вложений за период
turn_in_times = revenue / (ave_cash_and_CEB_period + ave_bal_of_STFI_period) # оборачиваемость в разах
print(f"Оборачиваемость в разах: {turn_in_times}")
```

20. `coefeldem()` - функция, считающая коэффициент эластичности спроса.
Код:

```python
I1_inc = float(input()) # величина дохода до изменения 
I2_inc = float(input()) # величина дохода после изменения
Q1_inc = float(input()) # величина спроса до изменения дохода
Q2_inc = float(input()) # величина спроса после изменения дохода
E_coef = ((Q2_inc - Q1_inc) / (Q2_inc + Q1_inc)) / (I2_inc - I1_inc) / (I2_inc + I1_inc) # коэффициент эластичности спроса
print(f"Коэффициент эластичности спроса: {E_coef}")
```    

21. `compinter_years()` - функция сложного процента, начисляемого за несколько лет.
Код:

```python
P_debt = float(input()) # сумма долга с процентами
k_years =  float(input()) # количество лет
ann_inter = float(input()) # годовой процент в долях
C_credit = P_debt * (1 + ann_inter) ** k_years # общая сумма кредита 
print(f"Сложный процент, начисляемый за несколько лет: {C_credit}")
```

22. `compinter()` - функция сложного процента.
Код:

```python
P_debt = float(input()) # сумма долга с процентами
n_days = float(input()) # количество дней
ann_inter = float(input()) # годовой процент в долях
k_years =  float(input()) # количество лет
C_credit = P_debt * (1 + ann_inter * n_days / 360) ** k_years # общая сумма кредита 
print(f"Сложный процент: {C_credit}")
```

23. `elofdem()` - функция, считающая эластичность спроса.
Код:

```python
Q1 = float(input()) # величина спроса по прежней цене
Q2 = float(input()) # величина спроса по новой цене
P1 = float(input()) # прежняя цена 
P2 = float(input()) # новая цена
E = ((Q2-Q1) / Q1) / ((P2 / P1) / P1)  # эластичность спроса
print(f"Эластичность спроса: {E}")
```

24. `grossnat_product_1()` - функция, делающая расчёт валового национального продукта (по потоку расходов).
Код:

```python
pers_exp = float(input()) # личные расходы
gover_proc = float(input()) # госзакупки
priv_invest = float(input()) # частные инвестиции
ner_exports = float(input()) # чистый экспорт
gro_nat_product = pers_exp + gover_proc + priv_invest + ner_exports # ВНП
print(f"Валовый национальный продукт: {gro_nat_product}")
```

25. `grossnat_product_2()` - функция, делающая расчёт валового национального продукта (по потоку доходов).
Код:

```python
depreciation = float(input()) # амортизация
indir_taxes = float(input()) # косвенные налоги
salary = float(input()) # зарплата
rent = float(input()) # рента
bank_inter = float(input()) # банковский процент
prof = float(input()) # прибыль
gro_nat_product = depreciation + indir_taxes + salary + rent + bank_inter + prof # ВНП
print(f"Валовый национальный продукт: {gro_nat_product}")
```

26. `dem_curve()` - функция, строящая график кривой спроса.
Код:

```python
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
```

27. `sup_curve()` - функция, строящая график кривой предложения.
Код:

```python
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
```

28. `budallocation_chart()` - функция, создающая круговую диаграмму распределения бюджета (доходы/расходы).
Код:

```python
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
```

29. `chartinc_exp_year()` - функция, создающая столбчатую диаграмму, которая показывает динамику изменения доходов и расходов в течение года.
Код:

```python
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
```

30. `forecastsales_year()` - функция, делающая прогнозирование продаж в течение года.
Код:

```python
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
```    