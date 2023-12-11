import time
from typing import Union
from dataclasses import dataclass
from copy import deepcopy

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
    times = [int(i) for i in lines[0].split(":")[1].split()]
    records = [int(i) for i in lines[1].split(":")[1].split()]
    part_1(times, records)
    time = int("".join([str(i) for i in times]))
    record = int("".join([str(i) for i in records]))
    part_2(time, record)

def part_1(times: list, records: list):
    result = 1
    for i in range(len(times)):
        possible = 0
        for j in range(times[i]):
            if j * (times[i] - j) > records[i]:
                possible += 1
        result *= possible
    print(f"Part 1: {result}")

def part_2(time: int, record: int):
    min_v = 0
    max_v = 0
    i = 1
    j = time - 1
    while i < time:
        if i * (time - i) > record:
            min_v = i
            break
        i += 1
    while j > 0:
        if j * (time - j) > record:
            max_v = j
            break
        j -= 1
    print(f"Part 2: {max_v - min_v + 1}")

if __name__ == "__main__":
    print(run_script("input.txt"))