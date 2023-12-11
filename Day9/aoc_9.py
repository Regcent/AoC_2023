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
    sequences = [[int(i) for i in line.split()] for line in lines]
    part_1(sequences)
    part_2(sequences)

def part_1(sequences: list):
    total = 0
    for sequence in sequences:
        total += find_next(sequence)
    print(f"Part 1: {total}")
    
def find_next(sequence: list):
    sub = []
    for i in range(len(sequence) - 1):
        sub.append(sequence[i + 1] - sequence[i])
    if len(sub) == sub.count(0):
        return sequence[-1]
    else:
        return sequence[-1] + find_next(sub)

def part_2(sequences: list):
    total = 0
    for sequence in sequences:
        total += find_next(sequence[::-1])
    print(f"Part 2: {total}")

if __name__ == "__main__":
    print(run_script("example.txt"))