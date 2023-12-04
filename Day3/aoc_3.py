import time
from typing import Union
from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Number:
    value: int
    delta_x: list
    y: int

    def neighbors(self) -> list:
        neighbors = list()
        for x in range(self.delta_x[0] - 1, self.delta_x[-1] + 2):
            neighbors.append((x, self.y - 1))
            neighbors.append((x, self.y + 1))
        neighbors.append((self.delta_x[0] - 1, self.y))
        neighbors.append((self.delta_x[-1] + 1, self.y))
        return neighbors

    def __str__(self) -> str:
        return f"{self.delta_x}, {self.y}: {self.value}"
@dataclass
class Schematic:
    numbers: list
    symbols: dict
    stars: dict   

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
    schematic = parse_schematic(lines)
    part_1(schematic)
    part_2(schematic)
    return 0

def parse_schematic(lines: list):
    numbers = {}
    symbols = {}
    stars = {}
    for y in range(len(lines)):
        numbers[y] = []
        symbols[y] = []
        stars[y] = []
        number = ""
        for x in range(len(lines[y])):
            if not lines[y][x].isnumeric():
                if number:
                    numbers[y].append(Number(int(number), list(range(x - len(number), x)), y))
                    number = ""
                if lines[y][x] == ".":
                    continue
                symbols[y].append(x)
                if lines[y][x] == "*":
                    stars[y].append(Number(-1, [x], y))
            if lines[y][x].isnumeric():
                number += lines[y][x]
        if number:
            numbers[y].append(Number(int(number), list(range(x - len(number), x)), y))
            number = ""
    return Schematic(numbers, symbols, stars)

def part_1(schematic):
    total = 0
    for key in schematic.numbers:
        for number in schematic.numbers[key]:
            for (x, y) in number.neighbors():
                if y not in schematic.symbols:
                    continue
                if x not in schematic.symbols[y]:
                    continue
                total += number.value
                break
    print(f"Part 1: {total}")

def part_2(schematic):
    total = 0
    for key in schematic.stars:
        for star in schematic.stars[key]:
            values = []
            for (x, y) in star.neighbors():
                if y not in schematic.numbers:
                    continue
                for number in schematic.numbers[y]:
                    if x not in number.delta_x:
                        continue
                    if number.value not in values:
                        values.append(number.value)
            if len(values) == 2:
                total += values[0] * values[1]
    print(f"Part 2: {total}")
                    
if __name__ == "__main__":
    print(run_script("input.txt"))