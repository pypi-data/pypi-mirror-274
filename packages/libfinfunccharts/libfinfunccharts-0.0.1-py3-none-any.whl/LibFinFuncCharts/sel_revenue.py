def selrevenue ():
    P_price = float(input()) # цена
    Q_quan = float(input()) # количество
    T_seller = P_price * Q_quan # выручка продавца
    print(f"Выручка продавца: {T_seller}")