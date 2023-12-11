import time
from typing import Union
from dataclasses import dataclass
from copy import deepcopy
import math

class Pipe:

    def __init__(self, value: str, x: int, y: int):
        self.vertical = False
        self.half = 0
        if value == ".":
            self.neighbors = None
        elif value == "|":
            self.neighbors = ((x, y - 1), (x, y + 1))
            self.vertical = True
        elif value == "-":
            self.neighbors = ((x - 1, y), (x + 1, y))
        elif value == "L":
            self.half = 1
            self.neighbors = ((x, y - 1), (x + 1, y))
        elif value == "J":
            self.half = 2
            self.neighbors = ((x, y - 1), (x - 1, y))
        elif value == "7":
            self.half = 1
            self.neighbors = ((x - 1, y), (x, y + 1))
        elif value == "F":
            self.half = 2
            self.neighbors = ((x + 1, y), (x, y + 1))
        elif value == "S":
            self.neighbors = ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))

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
    grid = parse_grid(lines)
    cycle = find_cycle(grid)
    print(f"Part 1: {(len(cycle) - 1) // 2}")
    replace_s(grid)
    part_2(grid, cycle)

def replace_s(grid: dict):
    s_x = grid["start"][0]
    s_y = grid["start"][1]
    """
    neighbors = grid["pipes"][s_y][s_x].neighbors
    valid_neighbors = []
    for neighbor in neighbors:
        n_x = neighbor[0]
        n_y = neighbor[1]
        if (s_x, s_y) in grid["pipes"][n_y][n_x].neighbors:
            valid_neighbors.append(n_x, n_y)
    if (x, y - 1) in valid_neighbors:
    """
    grid["pipes"][s_y][s_x] = Pipe("F", s_x, s_y)

def parse_grid(lines: list):
    grid = {"start": (0, 0), "pipes": []}
    for y in range(len(lines)):
        grid["pipes"].append([])
        for x in range(len(lines[y])):
            grid["pipes"][y].append(Pipe(lines[y][x], x, y))
            if lines[y][x] == "S":
                grid["start"] = (x, y)
    return grid

def find_cycle(grid: dict):
    trails = [[grid["start"]]]
    cycle = []
    while True:
        if cycle:
            break
        curr = trails.pop(0)
        neighbors = grid["pipes"][curr[-1][1]][curr[-1][0]].neighbors
        if len(curr) == 2:
            if not neighbors:
                continue
            if grid["start"] not in neighbors:
                continue
        for neighbor in neighbors:
            if invalid_neighbor(grid, neighbor):
                continue
            if len(curr) >= 2:
                if neighbor == curr[-2]:
                    continue
            if len(trails) == 1:
                if neighbor == trails[0][-1]:
                    cycle = trails[0] + curr[::-1]
            trails.append(curr + [neighbor])
    return cycle

def invalid_neighbor(grid: dict, neighbor: tuple):
    if neighbor[0] < 0 or neighbor[0] >= len(grid["pipes"][neighbor[1]]):
        return True
    if neighbor[1] < 0 or neighbor[1] >= len(grid["pipes"]):
        return True
    return False
        
def part_2(grid: dict, cycle: list):
    switch = {}
    halves = []
    for (x, y) in cycle:
        if grid["pipes"][y][x].vertical:
            if y not in switch:
                switch[y] = []
            switch[y].append(x)
        if grid["pipes"][y][x].half:
            if len(halves) == 0:
                halves.append((x, y))
            else:
                half_val = grid["pipes"][halves[0][1]][halves[0][0]].half
                if halves[0][1] == y:
                    if grid["pipes"][y][x].half != half_val:
                        halves = []
                        continue
                    if y not in switch:
                        switch[y] = []
                    switch[y].append(x) 
                else:
                    halves = [(x, y)]
    total = 0
    for y in range(len(grid["pipes"])):
        in_loop = False
        for x in range(len(grid["pipes"][y])):
            if y not in switch:
                break
            if x in switch[y]:
                in_loop = not in_loop
            if in_loop and (x, y) not in cycle:
                total += 1
    print(f"Part 2: {total}")

if __name__ == "__main__":
    print(run_script("input.txt"))