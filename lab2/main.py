import sys
import copy
import random

BOARD_SIZE = 15 # 15
CENTER = BOARD_SIZE // 2
WINNING_LENGTH = 5 # 5
MOVE_THREE_DISTANCE = 3 # 3
DEPTH_LIMIT = 5
EVAL_FUNC=1

def display(matrix):
    size = len(matrix)
    
    print(" ", end="")
    for i in range(size):
        print(f"  {i}", end="")
    print()
    print(" +" + "--+" * size)
    
    for i in range(size):
        if i > 0:
            print(" +" + "--+" * size)
        
        print(f"{i}", end="")
        for j in range(size):
            print("| " + matrix[i][j], end="")
        print("|")
    
    print(" +" + "--+" * size)

def get_moves(state):
    turn = 1
    moves = []

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if state[i][j] == " ":
                moves.append((i, j))
            else:
                turn += 1

    if turn == 1:
        return [(CENTER, CENTER)]
    
    if turn == 3:
        moves = list(filter(lambda x: abs(x[0] - CENTER) + (x[1] - CENTER) >= MOVE_THREE_DISTANCE, moves))

    random.shuffle(moves)
    return moves


def longest_stream(board, search):
    max_stream = 0

    def check_stream(row, col, dir_row, dir_col):
        stream_length = 0
        while 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == search:
            stream_length += 1
            row += dir_row
            col += dir_col
        return stream_length

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == search:
                directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                for dir_row, dir_col in directions:
                    stream_length = check_stream(i, j, dir_row, dir_col)
                    max_stream = max(max_stream, stream_length)

    return max_stream

def evaluation_function2(board):
    longest_x = longest_stream(board, "X")
    longest_o = longest_stream(board, "O")

    if longest_x >= WINNING_LENGTH:
        return WINNING_LENGTH * 2
    if longest_o >= WINNING_LENGTH:
        return -WINNING_LENGTH * 2

    return longest_x - longest_o

def evaluation_function1(board):
    def get_streams(search, not_search):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        streams = [0]

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == search:
                    for dir_row, dir_col in directions:
                        if 0 <= i - dir_row < BOARD_SIZE and 0 <= j - dir_col < BOARD_SIZE and board[i - dir_row][j - dir_col] == search:
                            continue
                        stream_length = 0
                        row = i
                        col = j
                        while 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == search:
                            stream_length += 1
                            row += dir_row
                            col += dir_col
                        row_cont = row
                        col_cont = col
                        current_length = stream_length
                        while 0 <= row_cont < BOARD_SIZE and 0 <= col_cont < BOARD_SIZE and board[row_cont][col_cont] != not_search and current_length < WINNING_LENGTH:
                            row_cont += dir_row
                            col_cont += dir_col
                            current_length += 1
                        if current_length >= WINNING_LENGTH:
                            streams.append(stream_length)
                        row_cont = i - dir_row
                        col_cont = j - dir_col
                        current_length = stream_length
                        while 0 <= row_cont < BOARD_SIZE and 0 <= col_cont < BOARD_SIZE and board[row_cont][col_cont] != not_search and current_length < WINNING_LENGTH:
                            row_cont -= dir_row
                            col_cont -= dir_col
                            current_length += 1
                        if current_length >= WINNING_LENGTH:
                            streams.append(stream_length)
        
        return streams

    x_streams = get_streams("X", "O")
    o_streams = get_streams("O", "X")

    x_max = max(x_streams)
    o_max = max(o_streams)

    if x_max + 1 >= WINNING_LENGTH:
        x_max *= 100

    if o_max + 1 >= WINNING_LENGTH:
        o_max *= 100

    x_streams = list(map(lambda x: x ** 2, x_streams))
    o_streams = list(map(lambda o: o ** 2, o_streams))

    x_max = x_max ** 2
    o_max = o_max ** 2

    x_sum = sum(x_streams)
    o_sum = sum(o_streams)
    
    x_rating = 10 * x_max + x_sum
    o_rating = 10 * o_max + o_sum

    return x_rating - o_rating


def alpha_beta(board, depth, alpha, beta, first_player, eval_func):
    if depth == 0 or longest_stream(board, 'X') >= WINNING_LENGTH or longest_stream(board, 'O') >= WINNING_LENGTH:
        return eval_func(board), None
    
    if first_player:
        max_eval = -sys.maxsize
        best_move = None
        for move in get_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = 'X'
            eval, _ = alpha_beta(new_board, depth - 1, alpha, beta, False, eval_func)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if max_eval >= beta:
                break
        return max_eval, best_move
    else:
        min_eval = sys.maxsize
        best_move = None
        for move in get_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = 'O'
            eval, _ = alpha_beta(new_board, depth - 1, alpha, beta, True, eval_func)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if min_eval <= alpha:
                break
        return min_eval, best_move

def get_best_move(board, eval_func):
    _, best_move = alpha_beta(board, DEPTH_LIMIT, -sys.maxsize, sys.maxsize, True, eval_func)
    return best_move
    

def override_globals():
    global BOARD_SIZE, DEPTH_LIMIT, WINNING_LENGTH, MOVE_THREE_DISTANCE, CENTER

    for arg in sys.argv[1:]:
        if arg.startswith("--size="):
            try:
                BOARD_SIZE = int(arg.split("=")[1])
                CENTER = BOARD_SIZE // 2
            except ValueError:
                print("Invalid value for --size. Using default value.")
        elif arg.startswith("--depth="):
            try:
                DEPTH_LIMIT = int(arg.split("=")[1])
            except ValueError:
                print("Invalid value for --depth. Using default value.")
        elif arg.startswith("--winning-length="):
            try:
                WINNING_LENGTH = int(arg.split("=")[1])
            except ValueError:
                print("Invalid value for --winning-length. Using default value.")
        elif arg.startswith("--move-three-distance="):
            try:
                MOVE_THREE_DISTANCE = int(arg.split("=")[1])
            except ValueError:
                print("Invalid value for --move-three-distance. Using default value.")
        elif arg.startswith('--eval-func='):
            try:
                EVAL_FUNC = int(arg.split("=")[1])
            except ValueError:
                print("Invalide value for --eval-func. Using default value.")

def game_is_draw(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == " ":
                return False
    return True

def main():
    override_globals()
    print(f"BOARD_SIZE={BOARD_SIZE} --size={BOARD_SIZE}")
    print(f"DEPTH_LIMIT={DEPTH_LIMIT} --depth={DEPTH_LIMIT}")
    print(f"WINNING_LENGTH={WINNING_LENGTH} --winning-length={WINNING_LENGTH}")
    print(f"MOVE_THREE_DISTANCE={MOVE_THREE_DISTANCE} --move-three-distance={MOVE_THREE_DISTANCE}, i.e. how far the first players second move from their first")
    print(f"EVAL_FUND={EVAL_FUNC} --eval_func={EVAL_FUNC}. 1 for evaluation function 1, any other int for evaluation function 2")
    print()
    print("Enter moves as y x. Example: 3 3")

    eval_func = evaluation_function1

    if EVAL_FUNC != 1:
        eval_func = evaluation_function2

    state = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    ai_turn = True
    while longest_stream(state, 'X') < WINNING_LENGTH and longest_stream(state, 'O') < WINNING_LENGTH:
        if game_is_draw(state):
            display(state)
            print("Draw. Good game!")
            return

        if ai_turn:
            move = get_best_move(state, eval_func)
            state[move[0]][move[1]] = 'X'
        else:
            display(state)
            move = tuple(map(lambda x: int(x), input("Move: ").strip(" ").split(" ")))
            state[move[0]][move[1]] = 'O'
        ai_turn = not ai_turn
    display(state)
    if longest_stream(state, 'X') >= WINNING_LENGTH:
        print("Player X won!")
    else:
        print("Player O won!")


if __name__ == "__main__":
    main()
