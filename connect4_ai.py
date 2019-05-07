import numpy as np
import time
DEPTH = 7 # DEPTH는 성능에 따라 조절
ROW_SIZE = 6
COLUMN_SIZE = 7
MAX_COUNT=9999999

def ai(board):      #turn 넣을지 말지 결정해야됩니다
    if np.sum(board[0,:]) == -7 :   # AI 가 선공일 때 4th column에 두면 안됩니다
        return 2                    # 4th가 아닌 3th column에 두도록
    else :
        start_time = time.time()
        bestCol = win_recursive(board, -MAX_COUNT, MAX_COUNT)
        print("--- %s seconds ---" %(time.time() - start_time))
        return bestCol

def win_recursive(board, alpha, beta, level=0):
    if (level == DEPTH):
        return evaluate(board,1)-evaluate(board,0)

    if (level % 2 == 0):
        array = np.full(COLUMN_SIZE, -MAX_COUNT)
        max_wincount = -MAX_COUNT
        for col_index in range(0, COLUMN_SIZE):
            if board[5, col_index] == -1 :
                child_board = copyChildBoard(board, col_index, level)
                if type(child_board) == bool and child_board == False:
                    array[col_index] = MAX_COUNT
                else:
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
        array = np.full(COLUMN_SIZE, MAX_COUNT)
        min_wincount = MAX_COUNT
        for col_index in range(0, COLUMN_SIZE):
            if board[5, col_index] == -1:
                child_board=copyChildBoard(board, col_index, level)
                if type(child_board) == bool and child_board == False:
                    array[col_index] = -MAX_COUNT
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

def evaluate(board,player):
    enemy= 0 if player == 1 else 1
    total_point=0
    for row in range(len(board)): #linetype -
        total_point+=pointByFeature(board[row],player)

    for column in range(COLUMN_SIZE): #linetype |
        row=np.append(board[:,column],[enemy])
        total_point+=pointByFeature(row,player)

    total_point+=pointByFeature(np.append(board[2:6,0:4].diagonal(),[enemy,enemy,enemy]),player) #linetype /
    total_point+=pointByFeature(np.append(board[1:6,0:5].diagonal(),[enemy,enemy]),player)
    total_point+=pointByFeature(np.append(board[0:6,0:6].diagonal(),[enemy]),player)
    total_point+=pointByFeature(np.append([enemy],board[0:6,1:7].diagonal()),player)
    total_point+=pointByFeature(np.append([enemy,enemy],board[0:5,2:7].diagonal()),player)
    total_point+=pointByFeature(np.append([enemy, enemy,enemy],board[0:4,3:7].diagonal()),player)

    total_point+=pointByFeature(np.append([enemy,enemy,enemy],np.fliplr(board[0:4,0:4]).diagonal()),player) #linetype \
    total_point+=pointByFeature(np.append([enemy,enemy],np.fliplr(board[0:5,0:5]).diagonal()),player)
    total_point+=pointByFeature(np.append([enemy],np.fliplr(board[0:6, 0:6]).diagonal()),player)
    total_point+=pointByFeature(np.append(np.fliplr(board[0:6, 1:7]).diagonal(),[enemy]),player)
    total_point+=pointByFeature(np.append(np.fliplr(board[1:6,2:7]).diagonal(),[enemy,enemy]),player)
    total_point+=pointByFeature(np.append(np.fliplr(board[2:6,3:7]).diagonal(),[enemy,enemy,enemy]),player)
    return total_point


def pointByFeature(row,player):
    start_idx = -1
    sum_point=0
    for idx, val in enumerate(row):
        if val == player and start_idx == -1:
            start_idx = idx

        if val != player and start_idx != -1:
            sum_point+=getPoint(row, player,start_idx, idx - 1)
            start_idx = -1
    return sum_point

def getPoint(row,player,start_idx,end_idx):
    chessman_num=end_idx-start_idx+1
    point=0
    enemy = 0 if player == 1 else 1
    if chessman_num==1:  #Feature4
        if start_idx ==0 or start_idx ==6:
            point+=4
        elif start_idx==1 or start_idx==5:
            point+=7
        elif start_idx==2 or start_idx==4:
            point+=12
        else:
            point+=20

    elif chessman_num==2:
        front_is_empty = start_idx-1>=0 and row[start_idx-1]!=enemy
        back_is_empty  = end_idx+1<7 and row[end_idx+1]!=enemy

        if front_is_empty and back_is_empty: #Feature2-4
            point += 5000

        if back_is_empty: #Feature 3
            temp = end_idx + 2
            if temp < 7 and row[temp] == player:  # Feature2-3
                point += 90000
            else:
                while temp<7:
                    if row[temp]==enemy:
                        break
                    point += 1000
                    temp +=1

        if front_is_empty: #Feature 3
            temp = start_idx - 2
            if temp >= 0 and row[temp] == player:  # Feature2-3
                point += 90000 #앞쪽으로만 2-3케이스를 추가하기위해
            else:
                while temp>=0:
                    if row[temp]==enemy:
                        break
                    point += 1000
                    temp -= 1

    elif chessman_num==3: #Feature 2
        if start_idx-1 >= 0 and row[start_idx-1] == -1:#Feature2-2
            if end_idx+1 < 7 and row[end_idx+1] == -1:#Feature2-1
                return MAX_COUNT
            point+=90000
        else:
            if end_idx+1 < 7 and row[end_idx + 1] == -1:#Feature2-2
                point += 90000

    elif chessman_num==4:
        return MAX_COUNT

    return point