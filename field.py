from ship import Ship, ShipCreationError


class ShipPlacementError(Exception):
    pass


class BattleField:
    SHIPS_COUNT = {3: 1, 2: 2, 1: 4}

    def __init__(self, *ships):
        self.field = self.create_empty_6x6_field()
        self.ships = []

        for ship in ships:
            self.add_ship_on_field(ship)

    @staticmethod
    def create_empty_6x6_field():
        field = []
        for _ in range(6):
            field.append([None] * 6)
        return field

    def add_ship_on_field(self, ship):
        if any(self.field[x][y] is not None for x, y in ship.points):
            raise ShipPlacementError(f'Unable to place {ship}')

        for x, y in ship.points:
            self.field[x][y] = 'S'
        for x, y in ship.space_around:
            self.field[x][y] = '~'

        self.ships.append(ship)

    def __str__(self):
        str_field = '  | 1 | 2 | 3 | 4 | 5 | 6 |\n'
        for num, line in enumerate(self.field, start=1):
            str_field += f'{num} | ' + ' | '.join(ch or '◯' for ch in line) + ' |\n'
        return str_field


def generate_random_field():
    from random import randint
    bf = BattleField()
    for ship_type, count in BattleField.SHIPS_COUNT.items():
        for _ in range(count):
            while True:
                try:
                    ship = Ship(randint(0, 5), randint(0, 5), ship_type, is_vertical=randint(0, 1))
                    bf.add_ship_on_field(ship)
                    # print(f'Created {ship}')
                    break
                except Exception as e:
                    pass
                    # print(e)

    return bf


if __name__ == '__main__':
    # bf = BattleField(Ship(0, 0, 3, is_vertical=False),
    #                  Ship(1, 3))
    # print('\n'.join(str(ship) for ship in bf.ships))
    # print(bf)
    # bf.add_ship_on_field(Ship(4, 4, 2, is_vertical=True))
    # print(bf)
    print(generate_random_field())
