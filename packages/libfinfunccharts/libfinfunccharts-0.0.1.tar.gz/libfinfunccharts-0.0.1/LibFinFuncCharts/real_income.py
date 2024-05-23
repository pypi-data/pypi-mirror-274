def realincome():
    nom_inc = float(input()) # номинальный доход
    con_price_ind = float(input()) # показатель индекса потребительских цен
    real_inc = nom_inc / con_price_ind * 100 # реальный доход
    print(f"Реальный доход: {real_inc}")