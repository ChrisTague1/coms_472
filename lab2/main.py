def display(state):
    for x in range(len(state)):
        for y in range(len(state[x])):
            print(state[x][y], end=" ")
        print()


def get_moves(state):
    turn = 1
    moves = []

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == "":
                moves.append((i, j))
            else:
                turn += 1

    if turn == 1:
        return [(8, 8)]
    
    if turn == 3:



def main():
    initial_state = [["" for _ in range(15)] for _ in range(15)]
    initial_state[8][8] = "X"
    initial_state[4][7] = "O"
    display(initial_state)


if __name__ == "__main__":
    main()
