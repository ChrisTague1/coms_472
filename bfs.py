from display import display
from typing import List, Callable
import time


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


def bfs(start: List[int], goal_state: List[int]):
    start_time = time.time()
    queue = [(start, [])]
    visited = [start]

    nodes = 1

    while len(queue) > 0:
        state, path = queue.pop(0)

        # if len(path) == 8:
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
