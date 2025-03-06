"""
Tic Tac Toe Player
"""

import copy
import math  # noqa: F401
from collections import Counter

X = "X"
O = "O"  # noqa: E741
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count, o_count = 0, 0
    # X goes first.
    if board == initial_state:
        return X
    # If the game is over it is noone's turn.
    elif winner(board) or terminal(board):
        return None
    else:
        # Count the number of X's and O's on the board.
        for row in board:
            x_count += Counter(row)[X]
            o_count += Counter(row)[O]
        # If O has had the same or more turns, it is X's turn.
        if x_count <= o_count:
            return X
        else:
            return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action")
    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows for winner.
    for row in board:
        counts = Counter(row)
        if counts[X] == 3:
            return X
        elif counts[O] == 3:
            return O
    # Check columns for winner.
    c0 = [board[0][0], board[1][0], board[2][0]]
    c1 = [board[0][1], board[1][1], board[2][1]]
    c2 = [board[0][2], board[1][2], board[2][2]]
    # Check diagonals for winner.
    d0 = [board[0][0], board[1][1], board[2][2]]
    d1 = [board[2][0], board[1][1], board[0][2]]
    for c in [c0, c1, c2, d0, d1]:
        counts = Counter(c)
        if counts[X] == 3:
            return X
        elif counts[O] == 3:
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    # It fhere are any EMPTY slots, the game is not over.
    for row in board:
        if EMPTY in row:
            return False
    # Full board and no winner == terminal board.
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    match winner(board):
        case "X":
            return 1
        case "O":
            return -1
        case _:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
