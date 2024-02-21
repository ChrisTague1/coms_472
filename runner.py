import json
import os
import subprocess

alg = 'IDS'
directory = 'Part3/L24/'

times = []
nodes = []

times = []
nodes = []

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    command = ['python', 'main.py', file_path, alg]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output_json = json.loads(result.stdout)
    times.append(output_json['time'])
    nodes.append(output_json['nodes'])

avg_time = sum(times) / len(times) if times else 0
avg_nodes = sum(nodes) / len(nodes) if nodes else 0

with open('the_output.txt', 'a') as file:
    file.write(f"Average Time: {avg_time}")
    file.write(f"Average Nodes: {avg_nodes}")

print("Average Time:", avg_time)
print("Average Nodes:", avg_nodes)
