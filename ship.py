class ShipCreationError(Exception):
    pass


class Ship:
    def __init__(self, x, y, decks=1, is_vertical=None):
        if not 0 <= x <= 5 or not 0 <= y <= 5:
            raise ShipCreationError(f'Unable to create ship with x, y = {x}, {y}')

        self.decks = decks
        self.is_vertical = is_vertical
        self.points = []
        for i in range(decks):
            if is_vertical:
                if x + i > 5:
                    raise ShipCreationError(f'Unable to create VERTICAL {decks}-decks ship with x = {x}')
                self.points.append((x + i, y))
            else:
                self.points.append((x, y + i))
                if y + i > 5:
                    raise ShipCreationError(f'Unable to create HORIZONTAL {decks}-decks ship with y = {y}')

    @property
    def space_around(self):
        space = set()
        space |= {(x - 1, y) for (x, y) in self.points if x > 0}
        space |= {(x + 1, y) for (x, y) in self.points if x < 5}
        space |= {(x, y - 1) for (x, y) in self.points if y > 0}
        space |= {(x, y + 1) for (x, y) in self.points if y < 5}
        space -= set(self.points)
        return list(sorted(space))

    def __repr__(self):
        direction = 'vertical ' if self.is_vertical else 'horizontal '
        if self.decks == 1:
            direction = ''
        return f'{self.decks}-decks {direction}ship: {self.points}'


if __name__ == '__main__':
    deck_3 = Ship(5, 5, 1, is_vertical=True)
    print(deck_3)
