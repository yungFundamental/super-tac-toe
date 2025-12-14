import board
import cell
import statistics

counter = 0
max_depth = 4
show_counter = False


# If a line is unwinnable or is empty, it receives the value of 0,
# if a line has one x/o in it, it receives the value of 3/-3
# if a line has two x/o's in it, it receives the value of 6/-6
def evaluate_line(cell_line):
    x_counter = 0
    o_counter = 0
    unwinnable_counter = 0
    for j in cell_line:
        if j[0] == cell.XO.x:
            x_counter += 1
        elif j[0] == cell.XO.o:
            o_counter += 1

        # j[0] == blank:
        elif j[1]:
            unwinnable_counter += 1
            break

    if (x_counter > 0 and o_counter > 0) or unwinnable_counter or (x_counter == 0 and o_counter == 0):
        # line is unwinnable / none of the cells were chosen (neutral)
        return 0

    elif x_counter == 1:
        return 3
    elif x_counter == 2:
        return 6
    elif o_counter == 1:
        return -3
    elif o_counter == 2:
        return -6

    if x_counter == 3 or o_counter == 3:
        return "hello"


# return a numeric score of the board, based on who's winning. the algorithm checks each of the 8 lines and gives it a
# score between (-6) to 6, the bigger the number the better the situation is for x, the smaller the number means the
# situation is preferable for o.
# The score of the board is the average of the scores of the lines.
def evaluate(main_board):
    main_board.winner()
    if main_board.won[0] != cell.XO.blank:
        return main_board.won[0].value
    if main_board.full():
        return cell.XO.blank.value
    # score_board is full of the winner of each cell of the main_board in each index
    # (full boolean do indicate if it is a tie)
    score_board = []
    prev_score_board = []
    for i in main_board.cells:
        prev_score_board.append(i.won)
        i.winner()
        unwinnable = False
        if i.won[0] == cell.XO.blank:
            unwinnable = i.full()
        score_board.append((i.won[0], unwinnable))

    main_board.winner()
    for i in range(9):
        main_board.cells[i].won = prev_score_board[i]
    if main_board.won[0] != cell.XO.blank:
        print("FIXED")
        return main_board.won[0].value
    # all 8 line values
    return statistics.mean(
        [evaluate_line(score_board[0:9:3]), evaluate_line(score_board[1:9:3]), evaluate_line(score_board[2:9:3]),
         evaluate_line(score_board[0:3:1]), evaluate_line(score_board[3:6:1]), evaluate_line(score_board[6:9:1]),
         evaluate_line(score_board[0:9:4]), evaluate_line(score_board[2:8:2])])


def minimax(main_board, depth, bot_shape, big_index=0, maximizing=True, specific_board=True):
    global counter
    counter += 1
    # print(counter)
    main_board.winner()
    if main_board.won[0] != cell.XO.blank:
        return main_board.won[0].value
    if main_board.full():
        return cell.XO.blank.value
    if depth == max_depth:
        return evaluate(main_board)

    if main_board.cells[big_index].full():
        specific_board = False
    if maximizing:
        best_score = -100
        if specific_board:
            for i in range(len(main_board.cells[big_index].cells)):
                if main_board.cells[big_index].cells[i].id == cell.XO.blank:
                    main_board.cells[big_index].cells[i].id = bot_shape
                    score = minimax(main_board, depth + 1, cell.reverse(bot_shape), big_index=i, maximizing=False)
                    main_board.cells[big_index].cells[i].id = cell.XO.blank
                    best_score = max(best_score, score)
        else:
            # The bot may choose any open cell in the main board
            for j in range(len(main_board.cells)):
                for i in range(len(main_board.cells[j].cells)):
                    if main_board.cells[j].cells[i].id == cell.XO.blank:
                        main_board.cells[j].cells[i].id = bot_shape
                        score = minimax(main_board, depth + 1, cell.reverse(bot_shape), big_index=i, maximizing=False)
                        main_board.cells[j].cells[i].id = cell.XO.blank
                        best_score = max(best_score, score)
        return best_score
    else:
        # minimizing
        best_score = 100
        if specific_board:
            for i in range(len(main_board.cells[big_index].cells)):
                if main_board.cells[big_index].cells[i].id == cell.XO.blank:
                    main_board.cells[big_index].cells[i].id = bot_shape
                    score = minimax(main_board, depth + 1, cell.reverse(bot_shape), big_index=i, maximizing=True)
                    main_board.cells[big_index].cells[i].id = cell.XO.blank
                    best_score = min(best_score, score)
        else:
            # The bot may choose any open cell in the main board
            for j in range(len(main_board.cells)):
                for i in range(len(main_board.cells[j].cells)):
                    if main_board.cells[j].cells[i].id == cell.XO.blank:
                        main_board.cells[j].cells[i].id = bot_shape
                        score = minimax(main_board, depth + 1, cell.reverse(bot_shape), big_index=i, maximizing=True)
                        main_board.cells[j].cells[i].id = cell.XO.blank
                        best_score = min(best_score, score)
        return best_score


def bot_move(main_board, bot_shape, big_index=0, specific_board=True):
    global counter
    maximizing = bot_shape == cell.XO.x
    if maximizing:
        best_score = -100
    else:
        best_score = 100
    if main_board.cells[big_index].full():
        specific_board = False
    if specific_board:
        for i in range(len(main_board.cells[big_index].cells)):
            if main_board.cells[big_index].cells[i].id == cell.XO.blank:
                main_board.cells[big_index].cells[i].id = bot_shape
                score = minimax(main_board, 1, cell.reverse(bot_shape), big_index=i, maximizing=not maximizing)
                main_board.cells[big_index].cells[i].id = cell.XO.blank

                if (maximizing and score > best_score) or (not maximizing and score < best_score):
                    best_score = score
                    best_move = big_index, i

    else:
        # The bot may choose any open cell in the main board
        for j in range(len(main_board.cells)):
            for i in range(len(main_board.cells[j].cells)):
                if main_board.cells[j].cells[i].id == cell.XO.blank:
                    main_board.cells[j].cells[i].id = bot_shape
                    score = minimax(main_board, 1, cell.reverse(bot_shape), big_index=i, maximizing=not maximizing)
                    main_board.cells[j].cells[i].id = cell.XO.blank
                    if (maximizing and score > best_score) or (not maximizing and score < best_score):
                        best_score = score
                        best_move = j, i
    if show_counter:
        print(f"{counter} nodes created")
    counter = 0
    return best_move
