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
    if player(board) == X:
        board_copy[action[0]][action[1]] = X
    else:
        board_copy[action[0]][action[1]] = O
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


def impending_winner(board):  # noqa: PLR0911
    """
    Returns action to block an impending winner.
    """
    playr = player(board)
    # Check rows for impending winner.
    for i in range(3):
        row = []
        for j in range(3):
            row.append(board[i][j])
        counts = Counter(row)
        if counts[playr] == 2 and None in row:
            indx = row.index(None)
            return (i, indx)
    # Check columns for impending winner.
    for i in range(3):
        col = []
        for j in range(3):
            col.append(board[j][i])
        counts = Counter(col)
        if counts[playr] == 2 and None in col:
            indx = col.index(None)
            return (indx, i)
    # Check for diagonals impending winner.
    diag1 = [board[0][0], board[1][1], board[2][2]]
    diag2 = [board[2][0], board[1][1], board[0][2]]
    counts = Counter(diag1)
    if counts[playr] == 2 and None in diag1:
        indx = diag1.index(None)
        match indx:
            case 0:
                return (0, 0)
            case 1:
                return (1, 1)
            case 2:
                return (2, 2)
    counts = Counter(diag2)
    if counts[playr] == 2 and None in diag2:
        indx = diag2.index(None)
        match indx:
            case 0:
                return (2, 0)
            case 1:
                return (1, 1)
            case 2:
                return (0, 2)
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


def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        minv = min_value(result(board, action))
        v = max(v, minv)
    return v


def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        maxv = max_value(result(board, action))
        v = min(v, maxv)
    return v


def get_x_action(board):
    lst = []
    for action in actions(board):
        res = result(board, action)
        if impending_winner(res):
            return impending_winner(res)
        lst.append((action, max_value(res)))
    optimal_action = lst[0][0]
    for i in range(1, len(lst)):
        if lst[i][1] > lst[i - 1][1]:
            optimal_action = lst[i][0]
    board = result(board, optimal_action)
    return optimal_action


def get_o_action(board):
    lst = []
    for action in actions(board):
        res = result(board, action)
        impwin = impending_winner(res)
        if impwin:
            return impwin
        lst.append((action, min_value(res)))
    optimal_action = lst[0][0]
    for i in range(1, len(lst)):
        if lst[i][1] < lst[i - 1][1]:
            optimal_action = lst[i][0]
    return optimal_action


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        optimal_action = get_x_action(board)
    elif player(board) == O:
        optimal_action = get_o_action(board)

    return optimal_action
