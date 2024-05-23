def compinter_years():
    P_debt = float(input()) # сумма долга с процентами
    k_years =  float(input()) # количество лет
    ann_inter = float(input()) # годовой процент в долях
    C_credit = P_debt * (1 + ann_inter) ** k_years # общая сумма кредита 
    print(f"Сложный процент, начисляемый за несколько лет: {C_credit}")