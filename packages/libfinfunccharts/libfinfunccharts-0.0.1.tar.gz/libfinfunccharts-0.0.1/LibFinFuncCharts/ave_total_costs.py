def avetotal_costs():
    tot_costs = float(input()) # общие издержки
    prod_vol = float(input()) # объём производства
    ave_tot_costs = tot_costs / prod_vol # средние общие издержки
    print(f"Средние общие издержки: {ave_tot_costs}")