import time
from typing import Union
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
import math

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    TOP = 3
    BOT = 4

class Position:

    def __init__(self, mirror: bool, ne: bool, splitter: bool, vertical: bool):
        self.mirror = mirror
        self.ne = ne
        self.splitter = splitter
        self.vertical = vertical

    def transform_direction(self, direction):
        if direction == Direction.RIGHT:
            return Direction.TOP if self.ne else Direction.BOT
        if direction == Direction.LEFT:
            return Direction.BOT if self.ne else Direction.TOP
        if direction == Direction.TOP:
            return Direction.RIGHT if self.ne else Direction.LEFT
        if direction == Direction.BOT:
            return Direction.LEFT if self.ne else Direction.RIGHT
    
    def split(self, direction):
        if direction == Direction.RIGHT or direction == Direction.LEFT:
            if self.vertical:
                return [Direction.TOP, Direction.BOT]
            else:
                return [direction]
        else:
            if self.vertical:
                return [direction]
            else:
                return [Direction.RIGHT, Direction.LEFT]

def new_pos(x: int, y: int, dir):
    if dir == Direction.RIGHT:
        return (x + 1, y)
    elif dir == Direction.LEFT:
        return (x - 1, y)
    elif dir == Direction.TOP:
        return (x, y - 1)
    else:
        return (x, y + 1)

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
    grid = []
    for y in range(len(lines)):
        line = []
        for x in range(len(lines[y])):
            if lines[y][x] == ".":
                line.append(Position(False, False, False, False))
            elif lines[y][x] == "/":
                line.append(Position(True, True, False, False))
            elif lines[y][x] == "\\":
                line.append(Position(True, False, False, False))
            elif lines[y][x] == "|":
                line.append(Position(False, False, True, True))
            elif lines[y][x] == "-":
                line.append(Position(False, False, True, False))
        grid.append(line)
    activated = solve(grid, (0, 0), Direction.RIGHT)
    print(f"Part 1: {len(activated)}")
    max_activated = len(activated)
    for init in [[(0, y), Direction.RIGHT] for y in range(1, len(grid))]:
        activated = solve(grid, *init)
        if len(activated) > max_activated:
            max_activated = len(activated)
    for init in [[(len(grid[0]) - 1, y), Direction.LEFT] for y in range(len(grid))]:
        activated = solve(grid, *init)
        if len(activated) > max_activated:
            max_activated = len(activated)
    for init in [[(x, 0), Direction.BOT] for x in range(len(grid))]:
        activated = solve(grid, *init)
        if len(activated) > max_activated:
            max_activated = len(activated)
    for init in [[(x, len(grid) - 1), Direction.TOP] for x in range(len(grid))]:
        activated = solve(grid, *init)
        if len(activated) > max_activated:
            max_activated = len(activated)
    print(f"Part 2: {max_activated}")
    
def solve(grid: list, src: tuple, s_dir):
    to_resolve = [(src, s_dir)]
    activated = dict()
    while to_resolve:
        ((x, y), dir) = to_resolve.pop(0)
        if x < 0 or x >= len(grid[0]):
            continue
        if y < 0 or y >= len(grid):
            continue
        if (x, y) in activated:
            if dir in activated[(x, y)]:
                continue
        if (x, y) not in activated:
            activated[(x, y)] = [dir]
        else:
            activated[(x, y)].append(dir)
        if grid[y][x].mirror:
            new_dir = grid[y][x].transform_direction(dir)
            to_resolve.append((new_pos(x, y, new_dir), new_dir))
            continue
        if grid[y][x].splitter:
            new_dirs = grid[y][x].split(dir)
            if len(new_dirs) == 2:
                to_resolve.append((new_pos(x, y, new_dirs[0]), new_dirs[0]))
                to_resolve.append((new_pos(x, y, new_dirs[1]), new_dirs[1]))
                continue
        to_resolve.append((new_pos(x, y, dir), dir))
    return activated
    
if __name__ == "__main__":
    print(run_script("input.txt"))