def grossnat_product_2():
    depreciation = float(input()) # амортизация
    indir_taxes = float(input()) # косвенные налоги
    salary = float(input()) # зарплата
    rent = float(input()) # рента
    bank_inter = float(input()) # банковский процент
    prof = float(input()) # прибыль
    gro_nat_product = depreciation + indir_taxes + salary + rent + bank_inter + prof # ВНП
    print(f"Валовый национальный продукт: {gro_nat_product}")