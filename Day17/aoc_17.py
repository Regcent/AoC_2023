import time
from typing import Union
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from queue import PriorityQueue
import math

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    TOP = 3
    BOT = 4

class Node:

    def __init__(self, x: int, y: int, last_directions: list, total_loss: int, dist: int):
        self.x = x
        self.y = y
        self.last_directions = last_directions
        self.total_loss = total_loss
        self.dist = dist

    def __str__(self):
        return f"{self.path}"
    
    def __lt__(self, other):
        return self.total_loss + self.dist < other.total_loss + other.dist

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
            line.append(int(lines[y][x]))
        grid.append(line)
    part_1(grid)

def part_1(grid: list):
    start_pos = (0, 0)
    end_pos = (len(grid[0]) - 1, len(grid) - 1)
    pq = PriorityQueue()
    dist = distance(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
    pq.put(Node(start_pos[0], start_pos[1], [-1], 0, dist))
    explored = set()
    while not pq.empty():
        (node) = pq.get()
        if (node.x, node.y) == end_pos:
            break
        explored.add((node.x, node.y))
        for direction in Direction:
            if len(node.last_directions) == 3 and direction == node.last_directions[-1]:
                continue
            new = new_pos(node.x, node.y, direction)
            if new in explored:
                continue
            if not valid(new, len(grid[0]), len(grid)):
                continue
            dist = distance(new[0], new[1], end_pos[0], end_pos[1])
            print(dist)
            total_loss = node.total_loss + grid[new[1]][new[0]]
            last_directions = node.last_directions + [node.last_directions[-1]] if direction == node.last_directions[-1] else [direction]
            pq.put(Node(new[0], new[1], last_directions, total_loss, dist))
    print(node.total_loss)         

def valid(pos: tuple, max_x: int, max_y: int):
    if pos[0] < 0 or pos[0] >= max_x:
        return False
    if pos[1] < 0 or pos[1] >= max_y:
        return False
    return True

def distance(src_x: int, src_y: int, dst_x: int, dst_y: int):
    return abs(src_x - dst_x) + abs(src_y - dst_y)

if __name__ == "__main__":
    print(run_script("simple.txt"))