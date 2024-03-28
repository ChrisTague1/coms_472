import sys

BOARD_SIZE = 5 # 15
CENTER = BOARD_SIZE // 2 + 1
WINNING_LENGTH = 3 # 5
MOVE_THREE_DISTANCE = 1 # 3
DEPTH_LIMIT = 5

def display(state):
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            print(state[x][y], end="")
        print()


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
        return list(filter(lambda x: abs(x[0] - CENTER) + (x[1] - CENTER) >= MOVE_THREE_DISTANCE, moves))

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

# another similar one might involve squaring the the longest
def evaluation_function(board):
    longest_x = longest_stream(board, "X")
    longest_o = longest_stream(board, "O")

    if longest_x >= WINNING_LENGTH:
        return WINNING_LENGTH * 2
    if longest_o >= WINNING_LENGTH:
        return -WINNING_LENGTH * 2

    return longest_x - longest_o


def alpha_beta(board, depth, alpha, beta, first_player, eval_func):
    if depth == 0 or longest_stream(board, 'X') >= WINNING_LENGTH or longest_stream(board, 'O') >= WINNING_LENGTH:
        return eval_func(board), None
    
    if first_player:
        max_eval = -sys.maxsize
        best_move = None
        for move in get_moves(board):
            new_board = board.copy()
            new_board[move[0]][move[1]] = 'X'
            eval, _ = alpha_beta(new_board, depth - 1, alpha, beta, False, eval_func)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = sys.maxsize
        best_move = None
        for move in get_moves(board):
            new_board = board.copy()
            new_board[move[0]][move[1]] = 'O'
            eval, _ = alpha_beta(new_board, depth - 1, alpha, beta, True, eval_func)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_best_move(board, eval_func):
    _, best_move = alpha_beta(board, DEPTH_LIMIT, -sys.maxsize, sys.maxsize, True, eval_func)
    return best_move
    

def main():
    # first_player = input("Would you like to be player 1? T/F: ") == "T"
    # move = input("Enter the coordinates of your first move, space separated (ex. 4 9): ")
    # move = tuple(map(lambda x: int(x), move.strip(" ").split(" ")))
    # print(move)
    initial_state = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    initial_state[3][3] = 'X'
    initial_state[2][4] = 'O'
    initial_state[3][4] = 'X'
    initial_state[3][2] = 'O'
    display(initial_state)
    move = get_best_move(initial_state, evaluation_function)
    print(move)


if __name__ == "__main__":
    main()
