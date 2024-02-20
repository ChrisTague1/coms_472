import json
import os
from bfs import bfs
# from h2 import h2
import threading
import queue

alg = bfs


def call_and_store(initial_state, goal_state, result_queue):
    result = alg(initial_state, goal_state)
    result_queue.put(result)


def parse_file(file_path):
    puzzle = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            row = [int(x) if x != '_' else 0 for x in line.split()]
            puzzle.extend(row)
    return puzzle


GOAL_STATE = [
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
]
directory = 'Part3/L24/'

times = []
nodes = []
threads = []
result_queue = queue.Queue()

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    puzzle = parse_file(file_path)
    thread = threading.Thread(
        target=call_and_store,
        args=(puzzle, GOAL_STATE, result_queue))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

while not result_queue.empty():
    result = result_queue.get()
    output_json = json.loads(result)
    times.append(output_json['time'])
    nodes.append(output_json['nodes'])

avg_time = sum(times) / len(times) if times else 0
avg_nodes = sum(nodes) / len(nodes) if nodes else 0

print("Average Time:", avg_time)
print("Average Nodes:", avg_nodes)
