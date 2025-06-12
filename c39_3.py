import random

# Все возможные значения карт
cards = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'Валет': 10,
    'Дама': 10,
    'Король': 10,
    'Туз': [1, 11]
}

def draw_card():
    """Вытягивает случайную карту"""
    card = random.choice(list(cards.keys()))
    return card

def calculate_score(hand):
    """Считает очки в руке с учётом туза"""
    score = 0
    aces = 0
    
    for card in hand:
        if card == 'Туз':
            aces += 1
        else:
            score += cards[card]

    # Теперь обрабатываем тузы
    for _ in range(aces):
        if score + 11 <= 21:
            score += 11
        else:
            score += 1

    return score

def player_turn():
    """Ход игрока"""
    hand = [draw_card(), draw_card()]
    print(f"Ваши карты: {', '.join(hand)}")
    
    while True:
        score = calculate_score(hand)
        print(f"\nВаш счёт: {score}")
        
        if score > 21:
            print("Перебор!")
            return score
        
        action = input("Хотите взять ещё карту? (да/нет): ").strip().lower()
        if action == "да":
            new_card = draw_card()
            print(f"Вы получили: {new_card}")
            hand.append(new_card)
        elif action == "нет":
            break
        else:
            print("Введите 'да' или 'нет'.")
    
    return calculate_score(hand)

def computer_turn():
    """Ход компьютера (базовая логика)"""
    hand = [draw_card(), draw_card()]
    print(f"\nКарты компьютера: {hand[0]}, ???")

    while calculate_score(hand) < 17:
        hand.append(draw_card())

    score = calculate_score(hand)
    print(f"\nКарты компьютера: {', '.join(hand)}")
    print(f"Счёт компьютера: {score}")
    return score

def determine_winner(player_score, computer_score):
    """Определяет победителя"""
    if player_score > 21:
        return "Вы проиграли (перебор)."
    elif computer_score > 21:
        return "Компьютер проиграл (перебор). Вы выиграли!"
    elif player_score > computer_score:
        return "Вы выиграли!"
    elif player_score < computer_score:
        return "Компьютер выиграл."
    else:
        return "Ничья!"

def play_game():
    print("Добро пожаловать в игру 21 (Очко)!")

    player_score = player_turn()
    computer_score = computer_turn()

    print("\nРезультат:")
    print(determine_winner(player_score, computer_score))

# Запуск игры
if __name__ == "__main__":
    play_game()