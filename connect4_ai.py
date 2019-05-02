import numpy as np
import time
DEPTH = 7 # DEPTH는 성능에 따라 조절
ROW_SIZE = 6
COLUMN_SIZE = 7
MAX_COUNT=99999999

def ai(board):      #turn 넣을지 말지 결정해야됩니다
    if np.sum(board[0,:]) == -7 :   # AI 가 선공일 때 4th column에 두면 안됩니다
        return 2                    # 4th가 아닌 3th column에 두도록
    else :
        start_time = time.time() 
        bestCol = win_recursive(board, -MAX_COUNT, MAX_COUNT)
        print("--- %s seconds ---" %(time.time() - start_time))
        return bestCol

def win_recursive(board, alpha, beta,level=0):
    if (level == DEPTH):
        return wincount_h(board)

    if (level % 2 == 0):
        array = np.full(COLUMN_SIZE, MAX_COUNT)
        max_wincount = -MAX_COUNT
        for col_index in range(0, COLUMN_SIZE):
            if board[5, col_index] == -1 :
                child_board = copyChildBoard(board, col_index, level)
                if type(child_board) == bool and child_board == False:
                    array[col_index] = 700
                else :
                    array[col_index] = win_recursive(child_board, alpha, beta, level + 1)
                max_wincount = max(array[col_index], max_wincount)
                alpha = max(alpha, max_wincount)
                if beta <= alpha:
                    break
        if level == 0:
            print(array)
            return np.argmax(array)
        else:
            return max_wincount
    else:
        array = np.full(COLUMN_SIZE, -MAX_COUNT)
        min_wincount = MAX_COUNT
        for col_index in range(0, COLUMN_SIZE):
            if board[5, col_index] == -1:
                child_board=copyChildBoard(board, col_index, level)
                if type(child_board) == bool and child_board == False:
                    array[col_index] = -700
                else :
                    array[col_index] = win_recursive(child_board, alpha, beta, level + 1)
                min_wincount = min(array[col_index], min_wincount)
                beta = min(beta, min_wincount)
                if beta <= alpha:
                    break
        if level == 0:
            print(array)
            return np.argmax(array)
        else:
            return min_wincount

def copyChildBoard(parentBoard, col_index, level): #col_index 의 height만 알아내면 됩니다
    childBoard = np.copy(parentBoard)
    column_height = 0
    #if parentBoard[ROW_SIZE-1,col_index] == -1 :
        #column_height = ROW_SIZE
    #else :
        #column_height = np.argmin(parentBoard[:,col_index])
    for i in range(ROW_SIZE):
        if (parentBoard[i, col_index] == -1):
            column_height = i
            break


    # if (level % 2 == 0):  # 짝수인 경우 AI 차례!
    #     arr=[1,1,1,1]
    #     childBoard[column_height, col_index] = 1
    #
    # else:  # 홀수인 경우 상대방 차례
    #     arr[0,0,0,0]
    #     childBoard[column_height, col_index] = 0

    level_modulo_2=(level+1)%2
    childBoard[column_height, col_index] = level_modulo_2
    arr=[level_modulo_2 ,level_modulo_2 ,level_modulo_2 ,level_modulo_2 ]

    if column_height > 3 and childBoard[column_height - 3:column_height + 1, col_index].tolist() == arr: #linetype |
        return False

    for col in range(COLUMN_SIZE - 3): #linetype -
        if childBoard[column_height, col:col + 4].tolist() == arr:
            return False

    for column in range(COLUMN_SIZE - 3): #linetype /
        for row in range(ROW_SIZE - 3):
            if childBoard[row:row+4,column:column+4].diagonal().tolist()==arr:
                return False

    for column in range(COLUMN_SIZE - 3): #linetype \
        for row in range(3, ROW_SIZE):
            if childBoard[row][column] == level_modulo_2 and childBoard[row - 1][column + 1] == level_modulo_2 and childBoard[row - 2][
                column + 2] == level_modulo_2 and childBoard[row - 3][column + 3] == level_modulo_2:
                return False

    return childBoard


def wincount_h(board):  # 휴리스틱 함수  //  linetype 1:- 2:| 3:/ 4:\
                        # numpy array는 element 하나하나 접근하는것 보다 : 를 사용해서 범위로 접근하는것이 좋다고 합니다
                        # https://stackoverflow.com/questions/28357897/speeding-up-analysis-on-arrays-in-numpy 참고
    i = 0
    win_val_arr = np.zeros(69)
    lose_val_arr = np.zeros(69)
    for col in range(COLUMN_SIZE - 3):  # linetype : -
        for row in range(ROW_SIZE):
            win_val_arr[i] = win_casefunction(board[row,col:col+4].tolist())
            lose_val_arr[i] = lose_casefunction(board[row,col:col+4].tolist())
            i += 1
            #score += casefunction(board, row, column, 1)

    for col in range(COLUMN_SIZE):  # linetype : |
        for row in range(ROW_SIZE - 3):
            win_val_arr[i] = win_casefunction(board[row:row+4,col].tolist())
            lose_val_arr[i] = lose_casefunction(board[row:row+4,col].tolist())
            i += 1

    for col in range(COLUMN_SIZE - 3):  # linetype : /
        for row in range(ROW_SIZE - 3):
            win_val_arr[i] = win_casefunction(board[row:row+4,col:col+4].diagonal().tolist())
            lose_val_arr[i] = lose_casefunction(board[row:row+4,col:col+4].diagonal().tolist())
            i += 1

    for col in range(COLUMN_SIZE - 3):  # linetype : \ 이 대각선의 경우 flipud까지 사용해야해서 더 느려집니다
        for row in range(3, ROW_SIZE):  # np.flipud(board[row-4:row,col:col+4]).diagonal().tolist()
            win_val_arr[i] = win_casefunction([board[row][col], board[row-1][col+1], board[row-2][col+2], board[row-3][col+3]])
            lose_val_arr[i] = lose_casefunction([board[row][col], board[row-1][col+1], board[row-2][col+2], board[row-3][col+3]])
            i += 1

    return np.max(win_val_arr) + np.min(lose_val_arr)

def win_casefunction (list):        # 가중치(return 값)은 임의로 입력된 값으로 조정이 필요합니다                                                      
    if(list == [1, -1, -1, -1] or list == [-1, -1, -1, 1]):
        return 1
    elif(list == [-1, 1, -1, -1] or list == [-1, -1, 1, -1]):
        return 2
    elif(list == [1, 1, -1, -1] or list == [-1, -1, 1, 1]):
        return 9
    elif(list == [1, -1, 1, -1] or list == [-1, 1, -1, 1]):
        return 7
    elif(list == [1, -1, -1, 1]):
        return 5
    elif(list == [-1, 1, 1, -1]):
        return 11
    elif(list == [1, 1, 1, -1] or list == [-1, 1, 1, 1]):
        return 500
    elif(list == [1, 1, -1, 1] or list == [1, -1, 1, 1]):
        return 300
    else:
        return 0

def lose_casefunction (list):        # 가중치(return 값)은 임의로 입력된 값으로 조정이 필요합니다                                                      
    if(list == [0, -1, -1, -1] or list == [-1, -1, -1, 0]):
        return -1
    elif(list == [-1, 0, -1, -1] or list == [-1, -1, 0, -1]):
        return -2
    elif(list == [0, -1, -1, 0]):
        return -5
    elif(list == [-1, 0, 0, -1]):
        return -11
    elif(list == [0, 0, 0, -1] or list == [-1, 0, 0, 0]):
        return -500
    elif(list == [0, 0, -1, 0] or list == [0, -1, 0, 0]):
        return -300
    else:
        return 0