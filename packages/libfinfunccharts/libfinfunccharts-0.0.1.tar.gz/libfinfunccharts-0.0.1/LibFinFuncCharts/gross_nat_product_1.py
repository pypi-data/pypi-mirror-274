def grossnat_product_1():
    pers_exp = float(input()) # личные расходы
    gover_proc = float(input()) # госзакупки
    priv_invest = float(input()) # частные инвестиции
    ner_exports = float(input()) # чистый экспорт
    gro_nat_product = pers_exp + gover_proc + priv_invest + ner_exports # ВНП
    print(f"Валовый национальный продукт: {gro_nat_product}")