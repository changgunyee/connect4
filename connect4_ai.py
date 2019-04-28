ROW_SIZE = 6
COLUMN_SIZE = 7

def ai(board):
    return 1

def wincount_h(board): # 휴리스틱 함수
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
            multi = board[row][column] * board[row + 1][column + 1] * board[row + 2][column + 2] * board[row + 3][column + 3] 
            if multi != 0:
                add = board[row][column] + board[row + 1][column + 1] + board[row + 2][column + 2] + board[row + 3][column + 3] 
                if multi == -1 and add == -2:
                    score += 1
                elif multi == 1 and add == 0:
                    score += 2 
                elif multi == -1 and add == 2:
                    score += 3

    for column in range(COLUMN_SIZE - 3):
        for row in range(3, ROW_SIZE):
            multi = board[row][column] * board[row - 1][column + 1] * board[row - 2][column + 2] * board[row - 3][column + 3]
            if multi != 0:
                add = board[row][column] + board[row - 1][column + 1] + board[row - 2][column + 2] + board[row - 3][column + 3]
                if multi == -1 and add == -2:
                    score += 1
                elif multi == 1 and add == 0:
                    score += 2 
                elif multi == -1 and add == 2:
                    score += 3
    return score