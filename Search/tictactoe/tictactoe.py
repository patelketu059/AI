"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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
    """
    Returns player who has the next turn on a board.
    """
    empty = True
    count = 0
   
    for r in range(3):
        for c in range(3):
            if board[r][c] != None:
                count += 1
    
    if count == 0:
        return X
    if count % 2 == 0:
        return X
    else:
        return O

    
    
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
   
    moves = set()
    for r in range(3):
        for c in range(3):
            if board[r][c] is None:
                moves.add((r,c))
                
    return moves
   
    



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid Action")

    newBoard = deepcopy(board)
    newBoard[action[0]][action[1]] = player(board)

    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                 return O
            else:
                return None
        
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == X:
                return X
            elif board[0][i] == O:
                 return O
            else:
                return None
    
    if (board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0]):
        if board[1][1] == X:
            return X
        elif board[1][1] == O:
            return O
        else:
            return None

    return None 


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for r in range(3):
        for c in range(3):
            if board[r][c] is None:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
     


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    Maximum = float("-inf")
    Minimum = float("inf")

    if terminal(board) == True:
        return None

    if player(board) == X:
        return max_x(board, Maximum, Minimum)[1]
    else:
        return min_o(board, Maximum, Minimum)[1]


def max_x(board, Maximum, Minimum):
    
    moves = actions(board)
    optimalAction = None

    if terminal(board):
        return [utility(board), None]

    v = float("-inf")

    for move in moves:
        currentBoard = result(board, move)
        if min_o(currentBoard, Maximum, Minimum)[0] > v:
            optimalAction = move
        v = max(v, min_o(currentBoard, Maximum, Minimum)[0])
        Maximum = max(v, min_o(currentBoard, Maximum, Minimum)[0])
        if Maximum >= Minimum:
            break

    return [v, optimalAction]
        


def min_o(board, Maximum, Minimum):
    moves = actions(board)
    optimalAction = None
    
    if terminal(board):
        return [utility(board), None]
    
    v = float("inf")

    for move in moves:
        currentBoard = result(board,move)
        if max_x(currentBoard, Maximum, Minimum)[0] < v:
            optimalAction = move
        v = min(v, (max_x(currentBoard, Maximum, Minimum))[0])
        Minimum = min(v, max_x(currentBoard, Maximum, Minimum)[0])
        if Maximum >= Minimum:
            break

    return [v, optimalAction]