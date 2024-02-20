import time
from queue import PriorityQueue


def heuristic(state, goal_state, cost):
    count = cost
    for i, n in enumerate(state):
        i2 = goal_state.index(n)
        x1, y1 = i % 3, i // 3
        x2, y2 = i2 % 3, i2 // 3
        count += ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
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


def h2(initial, goal_state):
    start_time = time.time()
    visited = [initial]
    queue = PriorityQueue()
    queue.put((0, (initial, [])))
    nodes = 0

    while not queue.empty():
        current_time = time.time()

        if current_time - start_time > 15 * 60:
            print("Timed out: runtime greater than 15 minutes")
            return

        nodes += 1
        _, (state, path) = queue.get()

        if state == goal_state:
            print(f'{{"time": {current_time - start_time}, "nodes": {nodes}}}')
            # print(f'Nodes Visited: {nodes}')
            # print(f'Time taken: {current_time - start_time}')
            # print(f'Path Length: {len(path)}')
            # path = ''.join(path)
            # print(f'Path: {path}')
            return f'{{"time": {current_time - start_time}, "nodes": {nodes}}}'

        for next_state, next_path in get_next_states(state):
            if next_state not in visited:
                visited.append(next_state)
                queue.put((
                    heuristic(next_state, goal_state, len(path)),
                    (next_state, path + [next_path])
                ))
