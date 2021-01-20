from field import generate_random_field


def game():
    ai_field = generate_random_field()
    print('AI field')
    print(ai_field)
    print()
    player_field = generate_random_field()
    print('PLAYER field')
    print(player_field)

    # while ai_field.has_ships() and player_field.has_ships():


if __name__ == '__main__':
    game()

