import random

def guess_the_number():
    print("Добро пожаловать в игру 'Угадай число'!")
    print("Я загадал число от 1 до 100. Попробуй угадать его!")

    # Загадываем число от 1 до 100
    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        try:
            user_guess = int(input("Введите ваше число: "))
            attempts += 1

            if user_guess < 1 or user_guess > 100:
                print("Пожалуйста, введите число от 1 до 100.")
                continue

            if user_guess < secret_number:
                print("Слишком мало! Попробуй больше.")
            elif user_guess > secret_number:
                print("Слишком много! Попробуй меньше.")
            else:
                print(f"Поздравляю! Вы угадали число {secret_number} за {attempts} попыток!")
                break
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите целое число.")

# Запускаем игру
guess_the_number()