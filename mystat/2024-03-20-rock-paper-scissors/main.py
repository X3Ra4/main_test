from random import choice

NAMES = {"к": "Каміння", "н": "Ножиці", "п": "Папір"}
BEATS = {"к": "н", "н": "п", "п": "к"}


def choose_item(bot=False):
    if bot:
        return choice(tuple(NAMES))
    while True:
        item = input("Каміння (к), ножиці (н) або папір (п): ").strip().lower()
        if item in NAMES:
            return item
        print("Введіть к, н або п.")


def full_name(item):
    return NAMES[item]


def claim_winner(player, bot):
    if player not in NAMES or bot not in NAMES:
        return None
    if player == bot:
        return "draw"
    return "player" if BEATS[player] == bot else "bot"


def main():
    player, bot = choose_item(), choose_item(bot=True)
    print(f"{full_name(player)} проти {full_name(bot)}")
    outcomes = {"player": "Ви виграли!", "bot": "Комп’ютер виграв!", "draw": "Нічия!"}
    print(outcomes[claim_winner(player, bot)])


if __name__ == "__main__":
    main()
