from collections import deque

# Define the goal state
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]  # 0 represents the empty space

# Define the function to check if a state is the goal state
def is_goal_state(state):
    return state == goal_state

# Define the function to generate neighboring states
def neighbors(state):
    neighbors = []
    i = state.index(0)
    if i % 4 > 0:
        new_state = state[:]
        new_state[i], new_state[i - 1] = new_state[i - 1], new_state[i]
        neighbors.append(new_state)
    if i % 4 < 3:
        new_state = state[:]
        new_state[i], new_state[i + 1] = new_state[i + 1], new_state[i]
        neighbors.append(new_state)
    if i // 4 > 0:
        new_state = state[:]
        new_state[i], new_state[i - 4] = new_state[i - 4], new_state[i]
        neighbors.append(new_state)
    if i // 4 < 3:
        new_state = state[:]
        new_state[i], new_state[i + 4] = new_state[i + 4], new_state[i]
        neighbors.append(new_state)
    return neighbors

# Define the BFS function
def bfs(initial_state):
    visited = set()
    queue = deque([(initial_state, [])])

    while queue:
        current_state, path = queue.popleft()

        if is_goal_state(current_state):
            return path + [current_state]

        visited.add(tuple(current_state))

        for neighbor_state in neighbors(current_state):
            if tuple(neighbor_state) not in visited:
                queue.append((neighbor_state, path + [current_state]))

    return None

# Example usage:
initial_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 0, 14, 15]  # Initial state of the puzzle
solution = bfs(initial_state)
if solution:
    print("Solution found in", len(solution) - 1, "moves:")
    for step, state in enumerate(solution):
        print("Step", step, ":", state)
else:
    print("No solution found.")
