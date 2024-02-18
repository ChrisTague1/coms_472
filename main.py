from typing import List, Callable
import sys
import time


def display(state: List[int]):
    for i in range(3):
        for j in range(3):
            item = state[i * 3 + j]
            item = item if item != 0 else '_'
            print(item, end=' ')
        print()
    print()


def check_up(state: List[int]) -> bool:
    index = state.index(0)
    return index <= 5


def up(state: List[int]):
    index = state.index(0)
    other = index + 3
    copy = state[:]
    copy[index] = copy[other]
    copy[other] = 0
    return (copy, "U")


def check_down(state: List[int]) -> bool:
    index = state.index(0)
    return index >= 3


def down(state: List[int]):
    index = state.index(0)
    other = index - 3
    copy = state[:]
    copy[index] = copy[other]
    copy[other] = 0
    return (copy, "D")


def check_left(state: List[int]) -> bool:
    index = state.index(0)
    return index % 3 != 2


def left(state: List[int]):
    index = state.index(0)
    other = index + 1
    copy = state[:]
    copy[index] = copy[other]
    copy[other] = 0
    return (copy, "L")


def check_right(state: List[int]) -> bool:
    index = state.index(0)
    return index % 3 != 0


def right(state: List[int]):
    index = state.index(0)
    other = index - 1
    copy = state[:]
    copy[index] = copy[other]
    copy[other] = 0
    return (copy, "R")


CheckFunc = Callable[[List[int]], bool]
MoveFunc = Callable[[List[int]], List[int]]


def get_available_actions(state: List[int]) -> List[MoveFunc]:
    checks: List[CheckFunc] = [check_up, check_down, check_left, check_right]
    moves: List[MoveFunc] = [up, down, left, right]

    return [moves[index] for index, check in enumerate(checks) if check(state)]


def parse_file(file_path):
    puzzle = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            row = [int(x) if x != '_' else 0 for x in line.split()]
            puzzle.extend(row)
    return puzzle


def is_solvable(state: List[int]) -> bool:
    inversions = 0
    for i, n in enumerate(state):
        for j in range(i + 1, 9):
            if state[j] == 0:
                continue
            if n > state[j]:
                inversions += 1
    return inversions % 2 == 0


def bfs(start: List[int], goal_state: List[int]):
    start_time = time.time()
    queue = [(start, [])]
    visited = [start]

    nodes = 1

    while len(queue) > 0:
        state, path = queue.pop(0)

        # if len(path) == 17:
        #     display(state)
        #     break

        if state == goal_state:
            end_time = time.time()
            print(f'Nodes Visited: {nodes}')
            print(f'Time taken: {end_time - start_time}')
            print(f'Path Length: {len(path)}')
            path = ''.join(path)
            print(f'Path: {path}')
            return

        actions = get_available_actions(state)
        states = [action(state) for action in actions]

        for value in states:
            nodes += 1
            if value[0] in visited:
                continue
            else:
                visited.append(value[0])
            queue.append((value[0], path + [value[1]]))


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    state = parse_file(sys.argv[1])

    if not is_solvable(state):
        display(state)
        print("Puzzle is not solvable")
        sys.exit(1)

    goal_state = [
        1, 2, 3,
        4, 5, 6,
        7, 8, 0
    ]

    bfs(state, goal_state)


if __name__ == '__main__':
    main()
