from field import ShotResult, generate_random_field, BattleField
from random import randint
from ship import Ship


def get_player_field():
    bf = BattleField()
    for ship_type, count in BattleField.REQUIRED_SHIPS_COUNT.items():
        print(f'Input {count} {ship_type}-decks ships:')
        print(f'Format: `x y h`, where x, y - coordinates of the first deck (1 - 6), h/v - horisontal/vertical')
        for i in range(count):
            while True:
                try:
                    input_str = input(f"Input {ship_type}-decks ship #{i+1}: ")
                    x, y, direction = input_str.split()
                    ship = Ship(int(x) - 1, int(y) - 1, ship_type, is_vertical=(direction == 'v'))
                    bf.add_ship_on_field(ship)
                    print(bf)
                    break
                except Exception as e:
                    print(e)

    return bf


def player_turn(ai_field):
    print('AI field')
    ai_field.print_without_ships()
    while True:
        x, y = map(int, input('Player, shoot `x y`: ').split())
        result = ai_field.shoot(x - 1, y - 1)
        if result == ShotResult.MISS:
            print('You missed!')
            ai_field.print_without_ships()
            input('Press Enter to continue...')
            break
        print('You hit something!')
        if result == ShotResult.DESTROYED:
            print("ship has been destroyed")
        ai_field.print_without_ships()
        if not ai_field.is_fleet_alive():
            print('You WIN!')
            return

def generate_new_x_y(attempts):
    x, y = randint(0, 5), randint(0, 5)
    while (x, y) in attempts:
        x, y = randint(0, 5), randint(0, 5)
    attempts.add((x, y))
    return x, y


def ai_turn(player_field, attempts):
    result = None
    while True:
        x, y = generate_new_x_y(attempts)
        result = player_field.shoot(x, y)
        if result == ShotResult.MISS:
            print('AI missed!')
            print(player_field)
            break
        print("AI hit something!")
        print(player_field)
        if not player_field.is_fleet_alive():
            print('AI WIN :C')
            break
    input('Press Enter to continue...')

def game():
    ai_field = generate_random_field()
    ai_attempts = set()
    player_field = generate_random_field()
    print('PLAYER field')
    print(player_field)

    while ai_field.is_fleet_alive() and player_field.is_fleet_alive():
        player_turn(ai_field)
        print()
        ai_turn(player_field, ai_attempts)
        print()


if __name__ == '__main__':
    game()

