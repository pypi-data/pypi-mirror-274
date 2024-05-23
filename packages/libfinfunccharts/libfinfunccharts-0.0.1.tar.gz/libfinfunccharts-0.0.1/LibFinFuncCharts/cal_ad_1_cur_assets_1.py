def calad_1_cur_assets_1():
    ave_bal_of_cur_assets_for_the_period = float(input()) # средние остатки оборотных активов за период
    numb_days_in_period = float(input()) # число дней в периоде (в месяце — 30, в квартале — 90, в году — 360)
    revenue = float(input()) # выручка
    ad_of_1_turn_of_cur_assets = (ave_bal_of_cur_assets_for_the_period*numb_days_in_period)/revenue # сред. про-сть 1-ого оборота об-ных активов
    print(f"Cредняя продолжительность одного оборота оборотных активов (в днях): {ad_of_1_turn_of_cur_assets}")