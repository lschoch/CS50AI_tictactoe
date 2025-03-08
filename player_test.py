import sys
from collections import Counter  # noqa: F401, INP001

from tictactoe import (  # noqa: F401
    actions,
    initial_state,
    player,
    result,
    terminal,
    utility,
    winner,
)

X = "X"
O = "O"  # noqa: E741
EMPTY = None

board = [
    [X, O, X],
    [X, O, X],
    [O, EMPTY, O],
]

action = (2, 1)
try:
    res = result(board, action)
except Exception as e:
    print(f"An error occurred: {e}. Exiting.")
    sys.exit()

print(res)
print(winner(res))
print(terminal(res))
print(utility(res))
