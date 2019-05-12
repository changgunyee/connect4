import numpy as np
import time

DEPTH = 8  # DEPTH는 성능에 따라 조절
ROW_SIZE = 6
COLUMN_SIZE = 7
MAX_COUNT = 9999999
NOT_FIRST = 0
STORE_LV2_POINT = np.full(COLUMN_SIZE * COLUMN_SIZE * COLUMN_SIZE, -MAX_COUNT)
STORE_LV3_POINT = np.full(COLUMN_SIZE * COLUMN_SIZE, -MAX_COUNT)
STORE_NEXT_CHOICE = np.full(COLUMN_SIZE * COLUMN_SIZE, -MAX_COUNT)


def ai(board, person_choice):
    global NOT_FIRST
    global STORE_NEXT_CHOICE
    if np.sum(board[0, :]) == -7:   # AI 가 선공일 때 4th column에 두면 안됩니다
        return 2                    # 4th가 아닌 3th column에 두도록
    else:
        if (NOT_FIRST == 0):
            SEARCH_COLUMN = [3, 2, 4, 1, 5, 0, 6]
        else:
            SEARCH_COLUMN = np.argsort(-(STORE_NEXT_CHOICE[person_choice * 7: person_choice * 7 + 7]))
        print("person_choice : ", person_choice+1)
        print("STORE_NEXT_CHOICE에 저장된 값 : ", STORE_NEXT_CHOICE[person_choice * 7: person_choice * 7 + 7])
        print("COLUMN 검색하는 순서 : ", SEARCH_COLUMN)
        global DEPTH
        DEPTH=8
        left_time = 120
        first_start_time = time.time()
        while True:
            start_time = time.time()
            bestCol = win_recursive(board, -MAX_COUNT, MAX_COUNT, SEARCH_COLUMN)
            STORE_NEXT_CHOICE = STORE_LV2_POINT[bestCol * 49: bestCol * 49 + 49]
            NOT_FIRST = 1
            runing_time = time.time() - start_time
            left_time -= runing_time
            if left_time < 6 * runing_time or DEPTH > 14:
                break
            DEPTH += 1
            print(DEPTH,"의 깊이 만큼 search결과 저희 heuristic값은 위의 배열과 같습니다.",bestCol+1,"의 열에 수를 둘 경우 heuristic값이 MAX입니다. ")
        print("--- %s seconds ---" % (time.time() - first_start_time))

        return bestCol


def win_recursive(board, alpha, beta, SEARCH_COLUMN, level=0, parent_col=-1):
    if (level == DEPTH):
        return evaluate(board, 1) - evaluate(board, 0)

    if (level % 2 == 0):
        array = np.full(COLUMN_SIZE, -MAX_COUNT)
        max_wincount = -MAX_COUNT
        for col_index in SEARCH_COLUMN:
            if board[5, col_index] == -1:
                child_board = copyChildBoard(board, col_index, level)
                if type(child_board) == bool and child_board == False:
                    array[col_index] = MAX_COUNT
                else:
                    array[col_index] = win_recursive(child_board, alpha, beta, SEARCH_COLUMN, level + 1, col_index)
                max_wincount = max(array[col_index], max_wincount)
                alpha = max(alpha, max_wincount)
                if beta <= alpha:
                    break
        if level == 2:
            STORE_LV3_POINT[parent_col * 7: parent_col * 7 + 7] = array[:]

        if level == 0:
            max_point = -MAX_COUNT-1
            max_point_index = -1
            for i in range(0, COLUMN_SIZE):
                if board[5, i] != -1:
                    array[i] = -MAX_COUNT - 1
            print(array)
            for i in [3, 2, 4, 1, 5, 0, 6]:
                if max_point < array[i]:
                    max_point = array[i]
                    max_point_index = i
            return max_point_index
        else:
            return max_wincount

    else:
        array = np.full(COLUMN_SIZE, MAX_COUNT)
        min_wincount = MAX_COUNT
        for col_index in SEARCH_COLUMN:
            if board[5, col_index] == -1:
                child_board = copyChildBoard(board, col_index, level)
                if type(child_board) == bool and child_board == False:
                    array[col_index] = -MAX_COUNT
                else:
                    array[col_index] = win_recursive(child_board, alpha, beta, SEARCH_COLUMN, level + 1, col_index)
                min_wincount = min(array[col_index], min_wincount)
                beta = min(beta, min_wincount)
                if beta <= alpha:
                    break
        if level == 1:
            STORE_LV2_POINT[parent_col * 49:parent_col * 49 + 49] = STORE_LV3_POINT[:]

        return min_wincount


def copyChildBoard(parentBoard, col_index, level):  # col_index 의 height만 알아내면 됩니다
    childBoard = np.copy(parentBoard)
    column_height = 0

    for i in range(ROW_SIZE):
        if (parentBoard[i, col_index] == -1):
            column_height = i
            break

    level_modulo_2 = (level + 1) % 2
    childBoard[column_height, col_index] = level_modulo_2
    arr = [level_modulo_2, level_modulo_2, level_modulo_2, level_modulo_2]

    if column_height >= 3 and childBoard[column_height - 3:column_height + 1, col_index].tolist() == arr:  # linetype |
        return False

    for col in range(COLUMN_SIZE - 3):  # linetype -
        if childBoard[column_height, col:col + 4].tolist() == arr:
            return False

    for column in range(COLUMN_SIZE - 3):  # linetype /
        for row in range(ROW_SIZE - 3):
            if childBoard[row:row + 4, column:column + 4].diagonal().tolist() == arr:
                return False

    for column in range(COLUMN_SIZE - 3):  # linetype \
        for row in range(3, ROW_SIZE):
            if childBoard[row][column] == level_modulo_2 and childBoard[row - 1][column + 1] == level_modulo_2 and \
                    childBoard[row - 2][column + 2] == level_modulo_2 and childBoard[row - 3][
                column + 3] == level_modulo_2:
                return False

    return childBoard


def evaluate(board, player):
    enemy = 0 if player == 1 else 1
    total_point = 0
    check_point = -1
    total_empty_count=0
    column_empty_count=[ 0 for column in range(COLUMN_SIZE)]
    for column in range(COLUMN_SIZE):
        for row in range(ROW_SIZE):
            if board[row][column]==-1:
                column_empty_count[column]=6-row
                total_empty_count+=6-row
                break
    for column in range(COLUMN_SIZE):
        column_empty_count[column]=total_empty_count-column_empty_count[column]

    for row in range(len(board)):                                                #linetype -
        temp, psbType = pointByFeature(board[row], player)
        check_point = checkPossible(psbType, board[row], player)
        if(psbType == -1 or check_point == -1):
            total_point += temp
        else:
            height = 0
            for i in range(0, row):
                if(board[i][check_point]==-1):               # = board[i][check_point] == -1
                    height += 1
            if((height + column_empty_count[check_point]) % 2 == 1):                #남은 수 = 해당 컬럼 제외 남은 수 + height, 가 짝수면 내가 못 놓음. 너나너나너나 로 끝나서 상대가 너로 놓게됨
                total_point += temp
            else:
                total_point += temp / 2

    for column in range(COLUMN_SIZE):                                           #linetype |
        row=np.append(board[:,column],[enemy])
        temp, psbType = pointByFeature(row,player,column)
        total_point += temp

    temp, psbType = pointByFeature(np.append(board[2:6,0:4].diagonal(), [enemy, enemy, enemy]), player) #linetype /
    check_point = checkPossible(psbType, np.append(board[2:6, 0:4].diagonal(), [enemy, enemy, enemy]), player)
    if(psbType == -1 or check_point == -1):
        total_point+= temp
    else:
        height = 0
        for i in range(0, check_point+2):
            if(board[i][check_point] == -1):
                height += 1
        if((height + column_empty_count[check_point]) % 2 == 1):
            total_point += temp
        else:
            total_point += temp / 2

    temp, psbType = pointByFeature(np.append(board[1:6,0:5].diagonal(),[enemy,enemy]),player)
    check_point = checkPossible(psbType, np.append(board[1:6, 0:5].diagonal(), [enemy, enemy]), player)
    if (psbType == -1 or check_point == -1):
        total_point += temp
    else:
        height = 0
        for i in range(0, check_point + 1):
            if (board[i][check_point] == -1):
                height += 1
        if((height +column_empty_count[check_point]) % 2 == 1):
            total_point += temp
        else:
            total_point += temp / 2

    temp, psbType = pointByFeature(np.append(board[0:6,0:6].diagonal(),[enemy]),player)
    check_point = checkPossible(psbType, np.append(board[0:6, 0:6].diagonal(), [enemy]), player)
    if (psbType == -1 or check_point == -1):
        total_point += temp
    else:
        height = 0
        for i in range(0, check_point):
            if (board[i][check_point] == -1):
                height += 1
        if((height + column_empty_count[check_point]) % 2 == 1):
            total_point += temp
        else:
            total_point += temp / 2

    temp, psbType = pointByFeature(np.append([enemy],board[0:6,1:7].diagonal()),player)
    check_point = checkPossible(psbType, np.append([enemy],board[0:6, 1:7].diagonal()), player)
    if (psbType == -1 or check_point == -1):
        total_point += temp
    else:
        height = 0
        for i in range(0, check_point - 1):
            if (board[i][check_point] == -1):
                height += 1
        if((height + column_empty_count[check_point]) % 2 == 1):
            total_point += temp
        else:
            total_point += temp / 2

    temp, psbType = pointByFeature(np.append([enemy,enemy],board[0:5,2:7].diagonal()), player)
    check_point = checkPossible(psbType, np.append([enemy,enemy],board[0:5, 2:7].diagonal()), player)
    if (psbType == -1 or check_point == -1):
        total_point += temp
    else:
        height = 0
        for i in range(0, check_point -2 ):
            if (board[i][check_point] == -1):
                height += 1
        if((height + column_empty_count[check_point]) % 2 == 1):
            total_point += temp
        else:
            total_point += temp / 2

    temp, psbType = pointByFeature(np.append([enemy, enemy, enemy],board[0:4,3:7].diagonal()),player)
    check_point = checkPossible(psbType, np.append([enemy, enemy, enemy],board[0:4, 3:7].diagonal()), player)
    if (psbType == -1 or check_point == -1):
        total_point += temp
    else:
        height = 0
        for i in range(0, check_point - 3):
            if (board[i][check_point] == -1):
                height += 1
        if((height + column_empty_count[check_point]) % 2 == 1):
            total_point += temp
        else:
            total_point += temp / 2

    temp, psbType = pointByFeature(np.append([enemy,enemy,enemy],np.fliplr(board[0:4,0:4]).diagonal()),player) #linetype \
    check_point = checkPossible(psbType, np.append([enemy, enemy, enemy],np.fliplr(board[0:4, 0:4]).diagonal()), player)
    if (psbType == -1 or check_point == -1):
        total_point += temp
    else:
        height = 0
        for i in range(0, check_point - 3):
            if (board[i][check_point] == -1):
                height += 1
        if((height + column_empty_count[3-check_point]) % 2 == 1):
            total_point += temp
        else:
            total_point += temp / 2

    temp, psbType = pointByFeature(np.append([enemy,enemy],np.fliplr(board[0:5,0:5]).diagonal()),player)
    check_point = checkPossible(psbType, np.append([enemy,enemy],np.fliplr(board[0:5, 0:5]).diagonal()), player)
    if (psbType == -1 or check_point == -1):
        total_point += temp
    else:
        height = 0
        for i in range(0, check_point - 2):
            if (board[i][check_point] == -1):
                height += 1
        if((height + column_empty_count[4-check_point]) % 2 == 1):
            total_point += temp
        else:
            total_point += temp / 2

    temp, psbType = pointByFeature(np.append([enemy],np.fliplr(board[0:6, 0:6]).diagonal()),player)
    check_point = checkPossible(psbType, np.append([enemy],np.fliplr(board[0:6, 0:6]).diagonal()), player)
    if (psbType == -1 or check_point == -1):
        total_point += temp
    else:
        height = 0
        for i in range(0, check_point - 1):
            if (board[i][check_point] == -1):
                height += 1
        if((height + column_empty_count[5-check_point]) % 2 == 1):
            total_point += temp
        else:
            total_point += temp / 2

    temp, psbType = pointByFeature(np.append(np.fliplr(board[0:6, 1:7]).diagonal(),[enemy]),player)
    check_point = checkPossible(psbType, np.append(np.fliplr(board[0:6, 1:7]).diagonal(),[enemy]), player)
    if (psbType == -1 or check_point == -1):
        total_point += temp
    else:
        height = 0
        for i in range(0, check_point):
            if (board[i][check_point] == -1):
                height += 1
        if((height + column_empty_count[6-check_point]) % 2 == 1):
            total_point += temp
        else:
            total_point += temp / 2

    temp, psbType = pointByFeature(np.append(np.fliplr(board[1:6,2:7]).diagonal(),[enemy,enemy]),player)
    check_point = checkPossible(psbType, np.append(np.fliplr(board[1:6, 2:7]).diagonal(), [enemy, enemy]), player)
    if (psbType == -1 or check_point == -1):
        total_point += temp
    else:
        height = 0
        for i in range(0, check_point + 1):
            if (board[i][check_point] == -1):
                height += 1
        if((height + column_empty_count[6 - check_point]) % 2 == 1):
            total_point += temp
        else:
            total_point += temp / 2

    temp, psbType = pointByFeature(np.append(np.fliplr(board[2:6,3:7]).diagonal(),[enemy,enemy,enemy]),player)
    check_point = checkPossible(psbType, np.append(np.fliplr(board[2:6, 3:7]).diagonal(), [enemy, enemy, enemy]), player)
    if (psbType == -1 or check_point == -1):
        total_point += temp
    else:
        height = 0
        for i in range(0, check_point + 2):
            if (board[i][check_point] == -1):
                height += 1
        if((height + column_empty_count[check_point]) % 2 == 1):
            total_point += temp
        else:
            total_point += temp / 2

    return total_point

def pointByFeature(row, player, column=-1):
    start_idx = -1
    sum_point = 0
    check_psb = -1                                      #getPoint 참조

    for idx, val in enumerate(row):
        if val == player and start_idx == -1:
            start_idx = idx

        if val != player and start_idx != -1:
            temp1, temp2 = getPoint(row, player,start_idx, idx - 1, column)
            sum_point += temp1
            check_psb = temp2
            start_idx = -1

    return sum_point, check_psb

def getPoint(row,player,start_idx,end_idx, column):
    chessman_num=end_idx-start_idx+1
    point=0
    check_possible = -1                        #기본 값 : -1, f 2-2 : 1, f 2-3 : 2
    enemy = 0 if player == 1 else 1
    front_is_empty = start_idx - 1 >= 0 and row[start_idx - 1] == -1
    back_is_empty = end_idx + 1 < 7 and row[end_idx + 1] == -1

    if chessman_num==1:  #Feature4
        if column == -1:
            column = start_idx
        if column == 0 or column == 6:
            point += 4
        elif column == 1 or column == 5:
            point += 7
        elif column == 2 or column == 4:
            point += 12
        else:
            point += 20

    elif chessman_num==2:
        if back_is_empty and (front_is_empty == False):  # Feature 3
            temp = end_idx + 2
            if temp < 7 and row[temp] == player:  # Feature2-3
                point += 90000
                check_possible = 2
            else:
                while temp < 7:
                    if row[temp] == enemy:
                        break
                    point += 500
                    temp += 1

        elif front_is_empty and (back_is_empty == False):  # Feature 3
            temp = start_idx - 2
            if temp >= 0 and row[temp] == player:  # Feature2-3
                point += 90000  # 앞쪽으로만 2-3케이스를 추가하기위해
                check_possible = 2
            else:
                while temp >= 0:
                    if row[temp] == enemy:
                        break
                    point += 500
                    temp -= 1

        elif front_is_empty and back_is_empty:  # Feature2-4
            temp1 = end_idx + 2
            temp2 = start_idx - 2
            if temp1 < 7 and row[temp1] == player and temp2 >= 0 and row[temp2] == player:
                point += 100000
                check_possible = 2
            else:
                point += 2500

    elif chessman_num==3: #Feature 2
        if front_is_empty: #Feature2-2
            if back_is_empty: #Feature2-1
                return 100000, 1
            point+=90000
            check_possible = 1
        else:
            if back_is_empty:#Feature2-2
                point += 90000
                check_possible = 1

    return point, check_possible

def checkPossible(psb, list, player):
    idx = -1
    if(psb == -1):
        return idx
    elif(psb == 1):
        for idx in range(0, 4):
            if(list[idx] == -1 and list[idx+1] == player and list[idx+2] == player and list[idx+3] == player):
                return idx
        for idx in range(3, 7):
            if(list[idx] == -1 and list[idx-1] == player and list[idx-2] == player and list[idx-3] == player):
                return idx
    elif(psb == 2):
        for idx in range(1, 5):
            if(list[idx-1] == player and list[idx] == -1 and list[idx+1] == player and list[idx+2] == player):
                return idx
        for idx in range(2, 6):
            if(list[idx-2] == player and list[idx - 1] == player and list[idx] == -1 and list[idx+1] == player):
                return idx