def calturn_days():
    revenue = float(input()) # выручка
    ave_cash_and_CEB_period = float(input()) # средние остатки денежных средств и денежных эквивалентов за период
    ave_bal_of_STFI_period = float(input()) # средние остатки краткосрочных финансовых вложений за период
    numb_days_in_period = float(input()) # число дней в периоде (в месяце — 30, в квартале — 90, в году — 360)
    turn_in_days = (ave_cash_and_CEB_period + ave_bal_of_STFI_period) * numb_days_in_period / revenue # оборачиваемость в днях
    print(f"Оборачиваемость в днях: {turn_in_days}")