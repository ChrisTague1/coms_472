import json
import os
import subprocess

alg = 'IDS'
directory = 'Part3/L24/'

times = []
nodes = []

times = []
nodes = []

# for filename in os.listdir(directory):
#     file_path = os.path.join(directory, filename)
#     command = ['python', 'main.py', file_path, alg]
#     result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#     output_json = json.loads(result.stdout)
#     times.append(output_json['time'])
#     nodes.append(output_json['nodes'])
#

with open('ids_output.txt', 'r') as file:
    for line in file:
        data = json.loads(line)
        times.append(data['time'])
        nodes.append(data['nodes'])

avg_time = sum(times) / len(times) if times else 0
avg_nodes = sum(nodes) / len(nodes) if nodes else 0

print("Average Time:", avg_time)
print("Average Nodes:", avg_nodes)
