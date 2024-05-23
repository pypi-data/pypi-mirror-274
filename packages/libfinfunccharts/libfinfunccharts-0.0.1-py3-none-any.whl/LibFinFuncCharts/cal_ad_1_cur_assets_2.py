def calad_1_cur_asset_2():
    ave_bal_of_cur_assets_for_the_period = float(input()) # средние остатки оборотных активов за период
    ave_daily_renuvue = float(input()) # среднедневная выручка
    ad_of_1_turn_of_cur_assets = ave_bal_of_cur_assets_for_the_period / ave_daily_renuvue # сред. про-сть 1-ого оборота об-ных активов
    print(f"Cредняя продолжительность одного оборота оборотных активов (в днях): {ad_of_1_turn_of_cur_assets}")