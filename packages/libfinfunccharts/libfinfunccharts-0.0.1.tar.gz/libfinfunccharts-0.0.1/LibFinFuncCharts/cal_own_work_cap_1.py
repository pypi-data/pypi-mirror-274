def calowm_work_cap_1():
    own_cap = float(input()) # собственный капитал
    ns_assets = float(input()) # внеоборотные активы
    owm_work_cap = own_cap - ns_assets # собственный оборотный капитал
    print(f"Собственный оборотный капитал: {owm_work_cap}") 