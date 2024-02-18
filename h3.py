import time
from queue import PriorityQueue


def get_neighbors(state, index):
    l, right, top, bottom = index - 1, index + 1, index - 3, index + 3
    if right >= len(state):
        right = right - len(state)
    if bottom >= len(state):
        bottom = bottom - len(state)
    l, right, top, bottom = state[l], state[right], state[top], state[bottom]
    return [l, right, top, bottom]


def heuristic(state, goal_state):
    count = 0
    for i, n in enumerate(state):
        neighbors = get_neighbors(state, i)
        goal_neighbors = get_neighbors(goal_state, i)
        for neighbor in neighbors:
            if neighbor not in goal_neighbors:
                count += 1
    return count


def get_next_states(state):
    states = []
    i = state.index(0)

    if i <= 5:
        next_state = state[:]
        next_state[i], next_state[i + 3] = next_state[i + 3], next_state[i]
        states.append((next_state, 'U'))
    if i >= 3:
        next_state = state[:]
        next_state[i], next_state[i - 3] = next_state[i - 3], next_state[i]
        states.append((next_state, 'D'))
    if i % 3 != 2:
        next_state = state[:]
        next_state[i], next_state[i + 1] = next_state[i + 1], next_state[i]
        states.append((next_state, 'L'))
    if i % 3 != 0:
        next_state = state[:]
        next_state[i], next_state[i - 1] = next_state[i - 1], next_state[i]
        states.append((next_state, 'R'))
    return states


def h3(initial, goal_state):
    start_time = time.time()
    visited = [initial]
    queue = PriorityQueue()
    queue.put((0, (initial, [])))
    nodes = 0

    while not queue.empty():
        nodes += 1
        _, (state, path) = queue.get()

        if state == goal_state:
            end_time = time.time()
            print(f'Nodes Visited: {nodes}')
            print(f'Time taken: {end_time - start_time}')
            print(f'Path Length: {len(path)}')
            path = ''.join(path)
            print(f'Path: {path}')
            return

        for next_state, next_path in get_next_states(state):
            if next_state not in visited:
                visited.append(next_state)
                queue.put((
                    heuristic(next_state, goal_state),
                    (next_state, path + [next_path])
                ))
