password_true = "qwerty"
name_true = 'Nina'

name = input("Введите имя - ")

if name_true == name:
    print(f"Имя пользователя введено верно - {name}")
    password = input("Введите пароль - ")
    if password_true == password:
        print(f"Пароль введен верно - {password}")
        print(f"Доступ в систему предоставлен")
    else:
        print("Неверно введен пароль - {password}")
else:
    print(f"Неверно введно имя - {name}")
