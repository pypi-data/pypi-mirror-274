def simpleinter():
    P_debt = float(input()) # сумма долга с процентами
    n_days = float(input()) # количество дней
    ann_inter = float(input()) # годовой процент в долях
    C_credit = P_debt * (1 + ann_inter * n_days / 360) # общая сумма кредита
    print(f"Простой процент: {C_credit}")