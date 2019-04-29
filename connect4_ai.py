import numpy as np

DEPTH = 5 # DEPTH는 성능에 따라 조절
ROW_SIZE = 6
COLUMN_SIZE = 7
MAX_COUNT=9999999999999

def ai(board):
    bestCol = win_recursive(board,-MAX_COUNT,MAX_COUNT)
    return bestCol


def win_recursive(board, alpha, beta,level=0):
    if (level == DEPTH):
        return wincount_h(board)

    array = np.full(COLUMN_SIZE, 0)

    if (level % 2 == 0):
        max_wincount=-MAX_COUNT
        for col_index in range(0, COLUMN_SIZE):
            array[col_index]=win_recursive(copyChildBoard(board, col_index, level), alpha, beta, level + 1)
            max_wincount=max(array[col_index],max_wincount)
            alpha = max(alpha, max_wincount)
            if beta <= alpha:
                break
        if level == 0:
            return np.argmax(array)
        else:
            return max_wincount
    else:
        min_wincount = MAX_COUNT
        for col_index in range(0, COLUMN_SIZE):
            array[col_index] = win_recursive(copyChildBoard(board, col_index, level), alpha, beta, level + 1)
            min_wincount = min(array[col_index], min_wincount)
            beta = min(beta, min_wincount)
            if beta <= alpha:
                break
        if level == 0:
            return np.argmax(array)
        else:
            return min_wincount


def copyChildBoard(parentBoard, col_index, level):
    childBoard = np.copy(parentBoard)
    column_height = [0 for num in range(COLUMN_SIZE)]
    for i in range(COLUMN_SIZE):
        for j in range(ROW_SIZE):
            if (parentBoard[j][i] == -1):
                column_height[i] = j
                break

    if column_height[col_index] >= ROW_SIZE or col_index < 0 or col_index >= COLUMN_SIZE:
        return False

    if (level % 2 == 0):  # 짝수인 경우 AI 차례!
        childBoard[column_height[col_index]][col_index] = 1
    else:  # 홀수인 경우 상대방 차례
        childBoard[column_height[col_index]][col_index] = 0
    column_height[col_index] += 1

    return childBoard


def wincount_h(board):  # 휴리스틱 함수
    score = 0
    for column in range(COLUMN_SIZE - 3):
        for row in range(ROW_SIZE):
            multi = board[row][column] * board[row][column + 1] * board[row][column + 2] * board[row][column + 3]
            if multi != 0:
                add = board[row][column] + board[row][column + 1] + board[row][column + 2] + board[row][column + 3]
                if multi == -1 and add == -2:
                    score += 1
                elif multi == 1 and add == 0:
                    score += 2
                elif multi == -1 and add == 2:
                    score += 3

    for column in range(COLUMN_SIZE):
        for row in range(ROW_SIZE - 3):
            multi = board[row][column] * board[row + 1][column] * board[row + 2][column] * board[row + 3][column]
            if multi != 0:
                add = board[row][column] + board[row + 1][column] + board[row + 2][column] + board[row + 3][column]
                if multi == -1 and add == -2:
                    score += 1
                elif multi == 1 and add == 0:
                    score += 2
                elif multi == -1 and add == 2:
                    score += 3

    for column in range(COLUMN_SIZE - 3):
        for row in range(ROW_SIZE - 3):
            multi = board[row][column] * board[row + 1][column + 1] * board[row + 2][column + 2] * board[row + 3][
                column + 3]
            if multi != 0:
                add = board[row][column] + board[row + 1][column + 1] + board[row + 2][column + 2] + board[row + 3][
                    column + 3]
                if multi == -1 and add == -2:
                    score += 1
                elif multi == 1 and add == 0:
                    score += 2
                elif multi == -1 and add == 2:
                    score += 3

    for column in range(COLUMN_SIZE - 3):
        for row in range(3, ROW_SIZE):
            multi = board[row][column] * board[row - 1][column + 1] * board[row - 2][column + 2] * board[row - 3][
                column + 3]
            if multi != 0:
                add = board[row][column] + board[row - 1][column + 1] + board[row - 2][column + 2] + board[row - 3][
                    column + 3]
                if multi == -1 and add == -2:
                    score += 1
                elif multi == 1 and add == 0:
                    score += 2
                elif multi == -1 and add == 2:
                    score += 3
    return score
