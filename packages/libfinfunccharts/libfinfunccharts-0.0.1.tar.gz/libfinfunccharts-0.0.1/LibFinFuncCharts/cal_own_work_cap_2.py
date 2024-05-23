def calowm_work_cap_2():
    own_cap = float(input()) # собственный капитал
    lt_obligations = float(input()) # долгосрочные обязательства
    ns_assets = float(input()) # внеоборотные активы
    owm_work_cap = own_cap + lt_obligations - ns_assets  # собственный оборотный капитал
    print(f"Собственный оборотный капитал: {owm_work_cap}") 
