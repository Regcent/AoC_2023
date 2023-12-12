import time
from typing import Union
from dataclasses import dataclass
from copy import deepcopy
import math

class Variant:

    def __init__(self, series: list, first_on: bool, last_on: bool, index: int, max_idx: int):
        self.series = series
        self.first_on = first_on
        self.last_on = last_on
        self.index = index
        self.max_idx = max_idx

    def new_zero(self):
        if self.series[-1] == 0:
            return Variant(deepcopy(self.series), self.first_on, self.last_on, self.index + 1, self.max_idx)
        else:
            return Variant(self.series + [0], self.first_on, self.last_on, self.index + 1, self.max_idx)

    def new_one(self):
        first_on = True if index == 0 else self.first_on
        last_on = True if index == max_idx else self.last_on
        new_series = deepcopy(self.series)
        new_series[-1] += 1
        return Variant(new_series, first_on, last_on, self.index + 1, self.max_idx)

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
    part_1(lines)

def part_1(lines: list):
    total = 0
    for line in lines:
        values, targets = line.split()
        targets = [int(i) for i in targets.split(",")]
        valid = count_valid_variants(values, targets)
        total += len(valid)
    print(f"Part 1: {total}")

def count_valid_variants(values: str, targets: list) -> int:
    variants = [([], 0)]
    valid = []
    while variants:
        (series, index) = variants.pop(0)
        if not valid_series(series, values, index, targets):
            continue
        if index == len(values):
            valid.append(series)
            continue
        if len(series) == 0:
            if values[index] == ".":
                variants.append(([0], index + 1))
            elif values[index] == "#":
                variants.append(([1], index + 1))
            else:
                variants.append(([0], index + 1))
                variants.append(([1], index + 1))
            continue
        if values[index] == ".":
            if series[-1] == 0:
                variants.append((deepcopy(series), index + 1))
            else:
                variants.append((series + [0], index + 1))
        elif values[index] == "#":
            new_series = deepcopy(series)
            new_series[-1] += 1
            variants.append((new_series, index + 1))
        else:
            if series[-1] == 0:
                variants.append((deepcopy(series), index + 1))
                new_series = deepcopy(series)
                new_series[-1] += 1
                variants.append((new_series, index + 1))
            else:
                variants.append((series + [0], index + 1))
                new_series = deepcopy(series)
                new_series[-1] += 1
                variants.append((new_series, index + 1))
    return valid

def valid_series(series: list, values: str, index: int, targets: list):
    i = 0
    while i < len(series):
        if i >= len(targets):
            if series[i] != 0:
                return False
        else:
            if series[i] > targets[i]:
                 return False
            if i < len(series) - 1:
                if series[i] < targets[i]:
                    return False
            if index == len(values):
                if series[i] < targets[i]:
                    return False
        i += 1
    left_overs = 0
    for j in range(i, len(targets)):
        left_overs += targets[j]
    return left_overs <= len(values) - index

if __name__ == "__main__":
    print(run_script("input.txt"))