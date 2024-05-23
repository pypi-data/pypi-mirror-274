def calinv_turn_times():
    cost_of_sales = float(input()) # себестоимость продаж
    ave_stock_bal_period = float(input()) # средние остатки запасов за период
    inv_turn_in_times = cost_of_sales / ave_stock_bal_period # оборачиваемость запасов в разах
    print(f"Оборачиваемость запасов в разах: {inv_turn_in_times}")
