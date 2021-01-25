from enum import Enum
from random import randint

from ship import Ship, ShipCreationError


class ShipPlacementError(Exception):
    pass


class AlreadyShotError(Exception):
    pass


class ShotResult(Enum):
    MISS = 0
    DAMAGED = 1
    DESTROYED = 2


class BattleField:
    REQUIRED_SHIPS_COUNT = {3: 1, 2: 2, 1: 4}
    DISPLAY_MAPPING = {
        None: '◯',  # water
        'S': '■',   # ship
        'x': 'x',   # damaged deck
        'X': 'X',   # destroyed
        'M': 'T',   # missed
    }

    HIDDEN_MAPPING = {
        None: '◯',  # water
        'S': '◯',  # ship
        'x': 'x',  # damaged deck
        'X': 'X',  # destroyed
        'M': 'T',  # missed
    }

    def __init__(self, *ships):
        self.field = self.create_empty_6x6_field()
        self.ships = []

        for ship in ships:
            self.add_ship_on_field(ship)

    def __str__(self):
        return self.field_to_string(self.DISPLAY_MAPPING)

    def print_without_ships(self):
        print(self.field_to_string(self.HIDDEN_MAPPING))

    def field_to_string(self, characters_mapping):
        str_field = '  | 1 | 2 | 3 | 4 | 5 | 6 |\n'
        for num, line in enumerate(self.field, start=1):
            str_field += f'{num} | '
            str_field += ' | '.join(characters_mapping.get(ch) or ch for ch in line)
            str_field += ' |\n'
        return str_field

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

        if self.is_ready():
            self.finalize()

    def is_ready(self):
        for ship_decks, required_count in self.REQUIRED_SHIPS_COUNT.items():
            if len([s for s in self.ships if s.decks == ship_decks]) < required_count:
                return False
        return True

    def finalize(self):
        for line in self.field:
            for i in range(len(line)):
                if line[i] == '~':
                    line[i] = None

    def __find_ship(self, x, y):
        ships = [ship for ship in self.ships if (x, y) in ship.points]
        return ships[0]

    def shoot(self, x, y):
        current = self.field[x][y]
        if current is None:
            self.field[x][y] = 'M'
            return ShotResult.MISS
        if current in ('x', 'X'):
            raise AlreadyShotError(f'Shooting error: ({x}, {y}) is already damaged')
        if current == 'S':
            target = self.__find_ship(x, y)
            target.hit(x, y)
            if target.is_destroyed:
                # repaint all ship in destroyed color
                for i, j in target.points:
                    self.field[i][j] = 'X'
                return ShotResult.DESTROYED
            self.field[x][y] = 'x'
            return ShotResult.DAMAGED

    def is_fleet_alive(self):
        return not all(s.is_destroyed for s in self.ships)


def generate_random_field():
    bf = BattleField()
    for ship_type, count in BattleField.REQUIRED_SHIPS_COUNT.items():
        for _ in range(count):
            while True:
                try:
                    ship = Ship(randint(0, 5), randint(0, 5), ship_type, is_vertical=randint(0, 1))
                    bf.add_ship_on_field(ship)
                    break
                except Exception as e:
                    pass

    return bf

