def voldeficit():
    Q_dem = float(input()) # величина спроса
    Q_prop = float(input()) # величина предложения
    vol_def = Q_dem - Q_prop # объём дефецита
    print(f"Объём дефицита: {vol_def}")