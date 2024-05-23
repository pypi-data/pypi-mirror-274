def calinv_turn_days():
    ave_stock_bal_period = float(input()) # средние остатки запасов за период
    cost_of_sales = float(input()) # себестоимость продаж
    numb_days_in_period = float(input()) # число дней в периоде (в месяце — 30, в квартале — 90, в году — 360)
    inv_turn_in_days = ave_stock_bal_period * numb_days_in_period / cost_of_sales # оборачиваемость запасов в днях
    print(f"Оборачиваемость запасов в днях: {inv_turn_in_days}")