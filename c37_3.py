password_true = "qwerty123"
password = ""
count = 0

while password != password_true and count < 5:
    password = input("Enter your password: ")
    count += 1
if count < 5:
    print("Доступ разрешён")
else:
    print("Вы израсходовали лимит попыток")