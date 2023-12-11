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
    empty_columns = list(range(len(lines) - 1, -1, -1))
    empty_rows = list(range(len(lines) - 1, -1, -1))
    galaxies = []
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "#":
                if x in empty_columns:
                    empty_columns.remove(x)
                if y in empty_rows:
                    empty_rows.remove(y)
                galaxies.append([x, y])
    part_1(deepcopy(galaxies), empty_columns, empty_rows)
    part_2(deepcopy(galaxies), empty_columns, empty_rows)

def part_1(galaxies: list, empty_columns: list, empty_rows: list):
    expand(galaxies, empty_columns, empty_rows, 1)
    total = total_distances(galaxies)
    print(f"Part 1: {total}")

def part_2(galaxies: list, empty_columns: list, empty_rows: list):
    expand(galaxies, empty_columns, empty_rows, 999999)
    total = total_distances(galaxies)
    print(f"Part 2: {total}")

def expand(galaxies: list, empty_columns: list, empty_rows: list, expansion: int):
    for x in empty_columns:
        for galaxy in galaxies:
            if galaxy[0] > x:
                galaxy[0] += expansion
    for y in empty_rows:
        for galaxy in galaxies:
            if galaxy[1] > y:
                galaxy[1] += expansion

def total_distances(galaxies: list):
    total = 0
    for i in range(len(galaxies) - 1):
        for j in range(i, len(galaxies)):
            total += abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1])
    return total

if __name__ == "__main__":
    print(run_script("input.txt"))