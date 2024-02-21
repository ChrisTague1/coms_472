import time


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


def bfs(initial, goal_state):
    start_time = time.time()
    visited = [initial]
    queue = [(initial, [])]
    nodes = 0

    while len(queue) > 0:
        current_time = time.time()

        if current_time - start_time > 15 * 60:
            print("Timed out: runtime greater than 15 minutes")
            return

        nodes += 1
        state, path = queue.pop(0)

        if state == goal_state:
            output = f'{{"time": {current_time - start_time}, "nodes": {nodes}}}'
            with open('bfs_output.txt', 'a') as file:
                file.write(output)
            print(f'{{"time": {current_time - start_time}, "nodes": {nodes}}}')
            # print(f'Nodes Visited: {nodes}')
            # print(f'Time taken: {current_time - start_time}')
            # print(f'Path Length: {len(path)}')
            # path = ''.join(path)
            # print(f'Path: {path}')
            return

        for next_state, next_path in get_next_states(state):
            if next_state not in visited:
                visited.append(next_state)
                queue.append((next_state, path + [next_path]))
