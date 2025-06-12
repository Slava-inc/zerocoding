import random

def rock_paper_scissors():
    print("Добро пожаловать в игру 'Камень, Ножницы, Бумага'!")
    print("Выберите свой вариант: 1 - Камень, 2 - Ножницы, 3 - Бумага")

    choices = {1: "Камень", 2: "Ножницы", 3: "Бумага"}
    user_score = 0
    computer_score = 0

    while True:
        try:
            user_choice = int(input("Ваш выбор (1/2/3): "))
            if user_choice not in [1, 2, 3]:
                print("Неверный ввод. Пожалуйста, выберите 1, 2 или 3.")
                continue

            computer_choice = random.randint(1, 3)

            print(f"Вы выбрали: {choices[user_choice]}")
            print(f"Компьютер выбрал: {choices[computer_choice]}")

            # Определяем победителя
            if user_choice == computer_choice:
                print("Ничья!")
            elif (
                (user_choice == 1 and computer_choice == 2) or
                (user_choice == 2 and computer_choice == 3) or
                (user_choice == 3 and computer_choice == 1)
            ):
                print("Вы выиграли раунд!")
                user_score += 1
            else:
                print("Компьютер выиграл раунд!")
                computer_score += 1

            print(f"Счёт: Вы — {user_score}, Компьютер — {computer_score}")

            play_again = input("Хотите сыграть ещё раз? (да/нет): ").strip().lower()
            if play_again != "да":
                print("Спасибо за игру!")
                break

        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите число 1, 2 или 3.")

# Запускаем игру
rock_paper_scissors()