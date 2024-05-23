def coefeldem():
    I1_inc = float(input()) # величина дохода до изменения 
    I2_inc = float(input()) # величина дохода после изменения
    Q1_inc = float(input()) # величина спроса до изменения дохода
    Q2_inc = float(input()) # величина спроса после изменения дохода
    E_coef = ((Q2_inc - Q1_inc) / (Q2_inc + Q1_inc)) / (I2_inc - I1_inc) / (I2_inc + I1_inc) # коэффициент эластичности спроса
    print(f"Коэффициент эластичности спроса: {E_coef}")    
