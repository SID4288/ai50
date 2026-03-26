"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    x=sum(row.count(X) for row in board)
    o=sum(row.count(O) for row in board)
    if x <= o:
        return X
    else:
        return O


def actions(board):
    actions=set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i,j))
    return actions      


def result(board, action):
    if action not in actions(board):
        raise Exception("Invalid action")
    new_board = [row.copy() for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None

def terminal(board):
    if winner(board) is not None:
        return True
    if all(cell is not EMPTY for row in board for cell in row):
        return True
    return False


def utility(board):
   if winner(board)==X:
       return 1
   elif winner(board)==O:
       return -1
   else:       return 0 


def minimax(board):
    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        best_score = -math.inf
        best_move = None
        for action in actions(board):
            score = min_value(result(board, action))
            if score > best_score:
                best_score = score
                best_move = action
        return best_move

    else:
        best_score = math.inf
        best_move = None
        for action in actions(board):
            score = max_value(result(board, action))
            if score < best_score:
                best_score = score
                best_move = action
        return best_move
    
def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v