from connect4_ai import *

ROW_SIZE = 6
COLUMN_SIZE = 7
board = np.full((ROW_SIZE, COLUMN_SIZE), -1)
column_height = [0 for num in range(COLUMN_SIZE)]
DRAW = 0
menu_str = "1 ~ 7번 중 컬럼 선택하세요."

"""AI는 1번, 사용자는 0번입니다."""
"""-1은 빈칸, 1은 AI, 0은 사용자입니다."""


def print_board():
    for row in range(len(board)):
        for column in range(len(board[ROW_SIZE - 1 - row])):
            if board[ROW_SIZE - 1 - row][column] == 0:
                print('|0', end='')
            elif board[ROW_SIZE - 1 - row][column] == 1:
                print('|X', end='')
            else:
                print('| ', end='')
        print("|")


def choose(column, user=1):  # AI가 두는것이 1
    column -= 1
    if column_height[column] >= ROW_SIZE:
        print("해당 column은 가득찼습니다. 다른 column을 선택해주세요")
        return 0, False
    if (column == -1 and user == 1) or sum(column_height) == 36:
        print("무승부입니다.")
        return 1, True
    if column < 0 or column >= COLUMN_SIZE:
        print("해당 column에는 둘 수 없습니다. 다른 column을 선택해주세요")
        return 0, False

    board[column_height[column]][column] = user
    column_height[column] += 1
    print_board()
    return 0, True


def is_game_over(user):
    for column in range(COLUMN_SIZE - 3):
        for row in range(ROW_SIZE):
            if board[row][column] == user and board[row][column + 1] == user and board[row][column + 2] == user and \
                    board[row][column + 3] == user:
                return True

    for column in range(COLUMN_SIZE):
        for row in range(ROW_SIZE - 3):
            if board[row][column] == user and board[row + 1][column] == user and board[row + 2][column] == user and \
                    board[row + 3][column] == user:
                return True

    for column in range(COLUMN_SIZE - 3):
        for row in range(ROW_SIZE - 3):
            if board[row][column] == user and board[row + 1][column + 1] == user and board[row + 2][
                column + 2] == user and board[row + 3][column + 3] == user:
                return True

    for column in range(COLUMN_SIZE - 3):
        for row in range(3, ROW_SIZE):
            if board[row][column] == user and board[row - 1][column + 1] == user and board[row - 2][
                column + 2] == user and board[row - 3][column + 3] == user:
                return True


first_person = int(input("선공:1, 후공:2  선택하세요. :"))
global person_choice
person_choice = -1
if first_person == 1:
    while True:
        person_choice = int(input(menu_str))
        while True:
            if (person_choice != 4):
                break
            print("선공은 4번 컬럼에 놓을수 없습니다")
            person_choice = int(input(menu_str))
        DRAW, ACCURATE_POS = choose(person_choice, 0)
        if ACCURATE_POS:  # 사람이 두는것이 0
            break

while True:
    print("AI가 밑에 처럼 놓았습니다.")
    while True:
        choice_ai = ai(np.copy(board), person_choice - 1)
        print("AI_choice : ", choice_ai + 1)
        DRAW, ACCURATE_POS = choose(choice_ai + 1)
        if ACCURATE_POS:  # AI가 두는것이 1
            break
    if DRAW == 1:
        break
    if is_game_over(1):
        print("AI가 승리하였습니다.")
        break

    while True:
        person_choice = int(input(menu_str))
        DRAW, ACCURATE_POS = choose(person_choice, 0)
        if ACCURATE_POS:
            break
    if DRAW == 1:
        break
    if is_game_over(0):
        print("당신이 승리하였습니다.")
        break