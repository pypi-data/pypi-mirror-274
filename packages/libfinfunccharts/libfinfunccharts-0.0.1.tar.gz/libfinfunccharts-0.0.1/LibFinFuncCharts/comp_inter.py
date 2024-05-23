def compinter():
    P_debt = float(input()) # сумма долга с процентами
    n_days = float(input()) # количество дней
    ann_inter = float(input()) # годовой процент в долях
    k_years =  float(input()) # количество лет
    C_credit = P_debt * (1 + ann_inter * n_days / 360) ** k_years # общая сумма кредита 
    print(f"Сложный процент: {C_credit}")