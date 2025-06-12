money = 5500
while True:
    money = money - 500
    print(f"Совершаем покупку. Баланс - {money}")
    if money <=0:
        break