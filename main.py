from typing import List, Callable
import sys


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
    return (copy, 'up')


def check_down(state: List[int]) -> bool:
    index = state.index(0)
    return index >= 3


def down(state: List[int]):
    index = state.index(0)
    other = index - 3
    copy = state[:]
    copy[index] = copy[other]
    copy[other] = 0
    return (copy, 'down')


def check_left(state: List[int]) -> bool:
    index = state.index(0)
    return index % 3 != 2


def left(state: List[int]):
    index = state.index(0)
    other = index + 1
    copy = state[:]
    copy[index] = copy[other]
    copy[other] = 0
    return (copy, 'left')


def check_right(state: List[int]) -> bool:
    index = state.index(0)
    return index % 3 != 0


def right(state: List[int]):
    index = state.index(0)
    other = index - 1
    copy = state[:]
    copy[index] = copy[other]
    copy[other] = 0
    return (copy, 'right')


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
    queue = [(start, ['start'])]

    while len(queue) > 0:
        state, path = queue.pop()

        if state == goal_state:
            return path

        actions = get_available_actions(state)
        states = [action(state) for action in actions]

        for value in states:
            queue.append((value[0], path + [value[1]]))

        break
    print(queue)


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
