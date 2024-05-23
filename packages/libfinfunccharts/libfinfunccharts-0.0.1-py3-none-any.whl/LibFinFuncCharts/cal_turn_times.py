def calturn_times():
    revenue = float(input()) # выручка
    ave_cash_and_CEB_period = float(input()) # средние остатки денежных средств и денежных эквивалентов за период
    ave_bal_of_STFI_period = float(input()) # средние остатки краткосрочных финансовых вложений за период
    turn_in_times = revenue / (ave_cash_and_CEB_period + ave_bal_of_STFI_period) # оборачиваемость в разах
    print(f"Оборачиваемость в разах: {turn_in_times}")
