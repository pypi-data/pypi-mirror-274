def profitcal():
    T_seller = float(input()) # совокупный доход (выручка продавца)
    T_costs = float(input()) # общие затраты
    P_profit = T_seller - T_costs # расчёт прибыли  
    print(f"Расчёт прибыли: {P_profit}")