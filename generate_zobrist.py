import random
from typing import Dict, Tuple

from dlgo.gotypes import Player, Point

MAX63 = 0x7fffffffffffffff

table: Dict[Tuple[Point, Player | None], int] = {}
empty_board = 0
for row in range(1, 20):
    for col in range(1, 20):
        for state in (None, Player.black, Player.white):
            table[Point(row, col), state] = random.randint(0, MAX63)

print('from typing import Dict, Tuple')
print('from .gotypes import Player, Point')
print('')
print("__all__ = ['HASH_CODE', 'EMPTY_BOARD']")
print('')
print('HASH_CODE: Dict[Tuple[Point, Player | None], int] = {')
for (pt, state), hash_code in table.items():
    print('    (%r, %s): %r,' % (pt, str(state), hash_code))
print('}')
print('')
print('EMPTY_BOARD = %d' % random.randint(empty_board, MAX63))