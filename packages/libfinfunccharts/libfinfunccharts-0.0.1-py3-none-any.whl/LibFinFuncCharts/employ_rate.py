def employrate():
    numb_of_emp = float(input()) # число занятых
    work_size = float(input()) # численность рабочей силы
    emp_rate = numb_of_emp / work_size * 100 # уровень занятости
    print(f"Уровень занятости: {emp_rate}")