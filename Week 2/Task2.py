import random

BOARD_SIZE = 10
LOSE_SEQUENCE_LENGTH = 5

squares = {}
computer_moves = []
user_moves = []
best_next_move = []
lose_combos = []
allowed_sequence_length = 0

def main():
    shift = BOARD_SIZE - LOSE_SEQUENCE_LENGTH
    # Функция генерации квадратов 5x5 для их дальнейшей оценки
    add_corners(0, shift, 0, shift)
    add_corners(0, shift, shift - 1, BOARD_SIZE - 1)
    add_corners(shift - 1, BOARD_SIZE - 1, 0, shift)
    add_corners(shift - 1, BOARD_SIZE - 1, shift - 1, BOARD_SIZE - 1)
    # Просчитать проигрышные комбинации для квадрата 5x5
    diagonal_1 = []
    diagonal_2 = []
    for i in range(LOSE_SEQUENCE_LENGTH):
        temp = []
        temp1 = []
        for j in range(LOSE_SEQUENCE_LENGTH):
            cell = (i, j)
            temp.append(cell)
            cell = (j, i)
            temp1.append(cell)
        diagonal_1.append(temp[i])
        diagonal_2.append(temp[len(temp) - 1 - i])
        lose_combos.append(temp)
        lose_combos.append(temp1)
    lose_combos.append(diagonal_1)
    lose_combos.append(diagonal_2)
    # Начать игру
    game()

def game():
    # Запросить ввод хода у пользователя
    print('Введите адрес ячейки в формате "строка столбец", чтобы сделать ход')
    while len(computer_moves) + len(user_moves) < BOARD_SIZE ** 2:
        while True:
            user_move = input().split()
            if not validate_move(user_move):
                print("Некорректный ход")
            else:
                break
        user_move = (user_move[0], user_move[1])
        user_moves.append(user_move)
        # После хода пользвателя проверить, нет ли среди ходов проигрышной комбинации
        # Если найдена проигрышная комбинация, игра прекращается
        if check_if_lose("user"):
            print("Вы проиграли")
            exit()
        else:
            # Определение квадрата или квадратов, в которых был сделан ход
            ranges = evaluate_move(user_move)
            best_square = []
            # Если квадрат один, попробовать выбрать его для хода
            if len(ranges) == 1:
                best_square = ranges[0]
            # Если квадратов несколько, выбрать из них тот, в котором наименьшее количество ходов компьютера
            elif len(ranges) > 1:
                min_used_cells = float("inf")
                for i in range(len(ranges)):
                    used_cells = evaluate_squares(ranges[i])
                    if len(used_cells) < min_used_cells:
                        min_used_cells = len(used_cells)
                        best_square = ranges[i]
            # Оценить возможность хода в выбранном квадрате
            # Если ход в этом квадрате невозможен, выбрать квадрат из общего числа,
            # в котором наименьшее число ходов компьютера
            safe_cells = find_next_move(best_square)
            if len(safe_cells) == 0:
                min_used_cells = float("inf")
                for i in squares:
                    used_cells = evaluate_squares(squares[i])
                    if len(used_cells) < min_used_cells:
                        min_used_cells = len(used_cells)
                        best_square = squares[i]
                safe_cells = find_next_move(best_square)
            if len(safe_cells) > 0:
                make_move(safe_cells, "normal")
            else:
                # Если квадратов больше не удаётся найти, сменить тактику
                # и следовать за ходами пользователя
                free_cells = find_free_cells()
                make_move(free_cells, "sticky")
        # После хода компьютера проверить, нет ли среди ходов проигрышной комбинации
        # Если найдена проигрышная комбинация, игра прекращается
        if check_if_lose("computer"):
            print("Компьютер проиграл")
            exit()
        print_matrix()
    if (len(computer_moves) == len(user_moves)) and (len(computer_moves) + len(user_moves) == BOARD_SIZE ** 2):
        print("Ничья")

def add_corners(i_start, i_stop, j_start, j_stop):
    count = 0
    while i_start <= i_stop:
        start = j_start
        while start <= j_stop:
            cell = (i_start, start)
            if not count in squares:
                squares[count] = []
            squares[count].append(cell)
            start += 1
            count += 1
        i_start += 1

def validate_move(move):
    if move[0].isdigit() and move[1].isdigit():
        move[0] = int(move[0])
        move[1] = int(move[1])
        if move[0] >= 0 and move[0] < BOARD_SIZE and move[1] >= 0 and move[1] < BOARD_SIZE:
            if not move in user_moves and not move in computer_moves:
                return True
    return False

def evaluate_move(user_move):
    ranges = []
    for i in range(len(squares)):
        for j in range(len(squares[i])):
            if user_move[0] == squares[i][j][0] and user_move[1] == squares[i][j][1]:
                ranges.append(squares[i])
    return ranges

def evaluate_squares(ranges):
    cells = []
    if len(computer_moves) > 0:
        for i in range(len(computer_moves)):
            if computer_moves[i][0] >= ranges[0][0] and computer_moves[i][0] <= ranges[3][0] and computer_moves[i][1] >= ranges[0][1] and computer_moves[i][1] >= ranges[3][1]:
                cells.append(computer_moves[i])
    return cells

def check_if_lose(player):
    if player == "user":
        moves = user_moves
    else:
        moves = computer_moves
    squares_per_row = BOARD_SIZE - LOSE_SEQUENCE_LENGTH + 1
    for i in range(len(squares)):
        shifted_combos = []
        horizontal_shift = int(i / squares_per_row)
        vertical_shift = int(i % squares_per_row)
        for j in range(len(lose_combos)):
            temp = []
            for k in range(len(lose_combos[j])):
                cell = (lose_combos[j][k][0] + horizontal_shift, lose_combos[j][k][1] + vertical_shift)
                temp.append(cell)
            shifted_combos.append(temp)
        for m in range(len(shifted_combos)):
            count = 0
            combo = []
            for n in range(len(shifted_combos[m])):
                if shifted_combos[m][n] in moves:
                    if not shifted_combos[m][n] in combo:
                        combo.append(shifted_combos[m][n])
                        count += 1
            if count == len(shifted_combos[m]):
                return True
    return False

def find_next_move(square):
    # Записать массив всех клеток квадрата
    cells = []
    for i in range(square[0][0], square[3][0] + 1):
        for j in range(square[0][1], square[3][1] + 1):
            cell = (i, j)
            cells.append(cell)
    # Убрать из квадрата все клетки, занятые противником
    # и клетки, находящиеся с ними на проигрышной горизонтали/вертикали/диагонали
    diagonal_indices = []
    id1 = 0
    step1 = LOSE_SEQUENCE_LENGTH + 1
    id2 = LOSE_SEQUENCE_LENGTH - 1
    step2 = LOSE_SEQUENCE_LENGTH - 1
    while id1 <= len(cells) and id2 <= len(cells):
        if not cells[id1] in diagonal_indices:
            diagonal_indices.append(cells[id1])
        if not cells[id2] in diagonal_indices:
            diagonal_indices.append(cells[id2])
        id1 += step1
        id2 += step2
    for i in range(len(diagonal_indices)):
        cells.remove(diagonal_indices[i])
    marked_cells = []
    for i in range(len(user_moves)):
        if user_moves[i] in cells:
            cells.remove(user_moves[i])
    for i in range(len(marked_cells)):
        if marked_cells[i] in cells:
            cells.remove(marked_cells[i])
    # Убрать те клетки, в которые есть уже ходы компьютера
    for i in range(len(computer_moves)):
        if computer_moves[i] in cells:
            cells.remove(computer_moves[i])
    safe_cells = []
    # Для оставшихся проверить соседние клетки
    # Если в них нет хода компьютера, то в этой клетке можно сделать ход
    for i in range(len(cells)):
        safe = True
        row = -1
        while row <= 1:
            column = -1
            while column <= 1:
                temp = (cells[i][0] + row, cells[i][1] + column)
                if temp in computer_moves:
                    safe = False
                column += 1
            row += 1
        if safe == True:
            safe_cells.append(cells[i])
    return safe_cells

def make_move(safe_cells, type):
    if type == "normal":
        if len(safe_cells) == 1:
            computer_moves.append(safe_cells[0])
        else:
            computer_moves.append(random.choice(safe_cells))
    else:
        if len(safe_cells) == 1:
            computer_moves.append(safe_cells[0])
        else:
            cells = []
            for i in range(len(safe_cells)):
                safe = False
                row = -1
                while row <= 1:
                    column = -1
                    while column <= 1:
                        temp = (safe_cells[i][0] + row, safe_cells[i][1] + column)
                        if not temp in user_moves:
                            safe = True
                        column += 1
                    row += 1
                if safe == True:
                    cells.append(safe_cells[i])
            computer_moves.append(random.choice(cells))

def print_matrix():
    print("| |", end="")
    for i in range(BOARD_SIZE):
        print(str(i) + "|", end="")
    print()
    for i in range((BOARD_SIZE + 1) * 2 + 1):
        print("_", end="")
    print()
    for i in range(BOARD_SIZE):
        print("|" + str(i) + "|", end="")
        for j in range(BOARD_SIZE):
            cell = (i, j)
            if cell in user_moves:
                print("X|", end="")
            elif cell in computer_moves:
                print("O|", end="")
            else:
                print("_|", end="")
        print()

def find_free_cells():
    cells = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            cell = (i, j)
            if not cell in user_moves and not cell in computer_moves:
                cells.append(cell)
    return cells

if __name__ == '__main__':
    main()
