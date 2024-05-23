def volsurplus():
    Q_prop = float(input()) # величина предложения
    Q_dem = float(input()) # величина спроса
    vol_sur = Q_prop - Q_dem # объём излишек
    print(f"Объём излишек: {vol_sur}")