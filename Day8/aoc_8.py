import time
from typing import Union
from dataclasses import dataclass
from copy import deepcopy
import math

def run_script(filepath: str) -> Union[int, str, float, bool]:
    with open(filepath, "r") as f:
        raw_data = f.read()
    return main_function(raw_data)

def main_function(raw_data: str) -> Union[int, str, float, bool]:
    start_time = time.time()
    result = your_script(raw_data)
    elapsed_time = time.time() - start_time
    print(f"Time elapsed : {elapsed_time}s")
    return result

def your_script(raw_data: str) -> Union[int, str, float, bool]:
    lines = raw_data.split("\n")
    instructions = lines[0]
    nodes = {}
    for line in lines[2:]:
        curr = line[:3]
        left = line[7:10]
        right = line[12:15]
        nodes[curr] = (left, right)
    #part_1(instructions, nodes)
    part_2(instructions, nodes)

def part_1(instructions: str, nodes: list):
    curr_node = "AAA"
    end_node = "ZZZ"
    count = 0
    while curr_node != end_node:
        if instructions[count % len(instructions)] == "R":
            curr_node = nodes[curr_node][1]
        else:
            curr_node = nodes[curr_node][0]
        count += 1
    print(f"Part 1: {count}")

def part_2(instructions: str, nodes: list):
    paths = []
    confirmed_cycles = []
    for node in nodes:
        if node.endswith("A"):
            paths.append([node])
    count = 0
    while True:
        right = False
        if instructions[count % len(instructions)] == "R":
            right = True
        to_remove = []
        for i in range(len(paths)):
            paths[i].append(nodes[paths[i][-1]][0] if not right else nodes[paths[i][-1]][1])
            if not paths[i][-1].endswith("Z"):
                continue
            if count < 2 or count % 2 == 0:
                continue
            if paths[i][len(paths[i]) - 1] == paths[i][len(paths[i]) // 2]:
                confirmed_cycles.append(deepcopy(paths[i]))
                to_remove.append(i)
        for i in range(len(to_remove)):
            del paths[to_remove[i] - i]
        if not paths:
            break
        count += 1
    lengths = []
    for cycle in confirmed_cycles:
        print(len(cycle))
        lengths.append(len(cycle) // 2)
    print(f"Part 2: {math.lcm(*lengths)}")

if __name__ == "__main__":
    print(run_script("input.txt"))