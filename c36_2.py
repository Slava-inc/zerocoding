has_money = True        # есть деньги
friend_pay = False     # друг не платит
is_sick = False         # не болен

if (has_money or friend_pay) and not is_sick:
    print("Идём в кино")
else:
    print("Не идём в кино")