import time
from typing import Union
from dataclasses import dataclass
from copy import deepcopy
import math

### TODO : PRoblem with valid INCOMPLETE variants (e.g finishing with 0 and using the new ONE)

class Variant:

    def __init__(self, series: list, first_on: bool, last_on: bool, index: int, max_idx: int):
        self.series = series
        self.first_on = first_on
        self.last_on = last_on
        self.index = index
        self.max_idx = max_idx

    def new_zero(self):
        if len(self.series) == 0:
            return Variant([0], self.first_on, self.last_on, self.index + 1, self.max_idx)
        if self.series[-1] == 0:
            return Variant(deepcopy(self.series), self.first_on, self.last_on, self.index + 1, self.max_idx)
        else:
            return Variant(self.series + [0], self.first_on, self.last_on, self.index + 1, self.max_idx)

    def new_one(self):
        if len(self.series) == 0:
            return Variant([1], True, self.last_on, self.index + 1, self.max_idx)
        last_on = True if self.index == self.max_idx else self.last_on
        new_series = deepcopy(self.series)
        new_series[-1] += 1
        return Variant(new_series, self.first_on, last_on, self.index + 1, self.max_idx)

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
    variants = part_1(lines)
    part_2(lines, variants)

def part_1(lines: list):
    total = 0
    variants = list()
    for line in lines:
        values, targets = line.split()
        targets = [int(i) for i in targets.split(",")]
        valid = count_valid_variants(values, targets)
        variants.append({"first_on": 0, "last_on": 0, "both": 0, "none": 0})
        for variant in valid:
            if variant.first_on and variant.last_on:
                variants[-1]["both"] += 1
            elif variant.first_on:
                variants[-1]["first_on"] += 1
            elif variant.last_on:
                variants[-1]["last_on"] += 1
            else:
                variants[-1]["none"] += 1
        total += len(valid)
    print(f"Part 1: {total}")
    return variants

def part_2(lines: list, variants: list):
    total = 0
    long_variants = list()
    for i in range(len(lines)):
        values, targets = lines[i].split()
        targets = [int(i) for i in targets.split(",")]
        valid = count_valid_variants("?" + values, targets)
        long_variants.append({"first_on": 0, "last_on": 0, "both": 0, "none": 0})
        for variant in valid:
            if variant.first_on and variant.last_on:
                long_variants[-1]["both"] += 1
            elif variant.first_on:
                long_variants[-1]["first_on"] += 1
            elif variant.last_on:
                long_variants[-1]["last_on"] += 1
            else:
                long_variants[-1]["none"] += 1
        print(variants, long_variants)
        associations = count_associations(variants, long_variants, i)
        print(associations)
        total += associations
    print(f"Part 2: {total}")

def count_associations(variants: list, long_variants: list, idx: int):
    associations = [([key], variants[idx][key]) for key in variants[idx]]
    total = 0
    while associations:
        (series, amount) = associations.pop(0)
        print(series, amount)
        if len(series) == 5:
            total += amount
            continue
        if amount == 0:
            continue
        valid = []
        if series[-1] == "both" or series[-1] == "last_on":
            valid = ["last_on", "none"]
        else:
            valid = ["first_on", "last_on", "both", "none"]
        for key in valid:
            associations.append((series + [key], amount * long_variants[idx][key]))
    return total

def count_valid_variants(values: str, targets: list) -> int:
    max_idx = len(values) - 1
    variants = [Variant([], False, False, 0, max_idx)]
    valid = []
    while variants:
        variant = variants.pop(0)
        if not valid_series(variant.series, values, variant.index, targets):
            continue
        if variant.index == len(values):
            valid.append(variant)
            continue
        if values[variant.index] == ".":
            variants.append(variant.new_zero())
        elif values[variant.index] == "#":
            variants.append(variant.new_one())
        else:
            variants.append(variant.new_zero())
            variants.append(variant.new_one())
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
    print(run_script("iso_example.txt"))