import time
from typing import Union
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
import math

@dataclass
class Rock:
    x: int
    y: int
    moving: bool

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
    rocks = list()
    max_y = len(lines)
    max_x = len(lines[0])
    for y in range(max_y):
        for x in range(max_x):
            if lines[y][x] == ".":
                continue
            elif lines[y][x] == "#":
                rocks.append(Rock(x, y, False))
            elif lines[y][x] == "O":
                rocks.append(Rock(x, y, True))
            else:
                print("ISSUE", lines[y][x])
    move_top(rocks)
    rocks.sort(key=lambda x: x.y)
    load = count_load(rocks, max_y)
    print(f"Part 1: {load}")
    i = 0
    while i < 1000000000:
        move_top(rocks)
        move_left(rocks)
        move_bot(rocks, max_y)
        move_right(rocks, max_x)
        i += 1
    new = count_load(rocks, max_y)
    print(f"Part 2: {new}")

def count_load(rocks: list, max_y: int):
    total = 0
    for rock in rocks:
        if not rock.moving:
            continue
        total += max_y - rock.y 
    return total

def move_top(rocks: list):
    vertical = dict()
    for rock in rocks:
        if rock.x not in vertical:
            vertical[rock.x] = [rock]
        else:
            vertical[rock.x].append(rock)
    for x in vertical:
        vertical[x].sort(key=lambda r:r.y)
        last_block = -1
        for rock in vertical[x]:
            if rock.moving:
                rock.y = last_block + 1
                last_block += 1
            else:
                last_block = rock.y

def move_bot(rocks: list, max_y: int):
    vertical = dict()
    for rock in rocks:
        if rock.x not in vertical:
            vertical[rock.x] = [rock]
        else:
            vertical[rock.x].append(rock)
    for x in vertical:
        vertical[x].sort(reverse=True, key=lambda r:r.y)
        last_block = max_y
        for rock in vertical[x]:
            if rock.moving:
                rock.y = last_block - 1
                last_block -= 1
            else:
                last_block = rock.y

def move_left(rocks: list):
    horizontal = dict()
    for rock in rocks:
        if rock.y not in horizontal:
            horizontal[rock.y] = [rock]
        else:
            horizontal[rock.y].append(rock)
    for y in horizontal:
        horizontal[y].sort(key=lambda r:r.x)
        last_block = -1
        for rock in horizontal[y]:
            if rock.moving:
                rock.x = last_block + 1
                last_block += 1
            else:
                last_block = rock.x

def move_right(rocks: list, max_x: int):
    horizontal = dict()
    for rock in rocks:
        if rock.y not in horizontal:
            horizontal[rock.y] = [rock]
        else:
            horizontal[rock.y].append(rock)
    for y in horizontal:
        horizontal[y].sort(reverse=True, key=lambda r:r.x)
        last_block = max_x
        for rock in horizontal[y]:
            if rock.moving:
                rock.x = last_block - 1
                last_block -= 1
            else:
                last_block = rock.x

def debug_print(rocks: list, max_x: int, max_y: int):
    grid = []
    for y in range(max_y):
        line = ["." for x in range(max_x)]
        grid.append(line)
    for rock in rocks:
        if rock.moving:
            grid[rock.y][rock.x] = "O"
        else:
            grid[rock.y][rock.x] = "#"
    print("\n".join(["".join(line) for line in grid]))


if __name__ == "__main__":
    print(run_script("example.txt"))