import time
from typing import Union
from dataclasses import dataclass
from copy import deepcopy

class TranslationRange:

    def __init__(self, dst_start: int, src_start: int, length: int):
        self.min = src_start
        self.max = src_start + length - 1
        self.delta = dst_start - src_start

    def to_transform(self, seed: int) -> bool:
        return seed >= self.min and seed <= self.max

    def transform(self, seed: int) -> int:
        return seed + self.delta

    def transform_range(self, seed_range):
        if seed_range.max < self.min or seed_range.min > self.max:
            return None
        if seed_range.min >= self.min and seed_range.max <= self.max:
            return SeedRange(seed_range.min + self.delta, seed_range.max + self.delta)
        if seed_range.min < self.min and seed_range.max <= self.max:
            return SeedRange(self.min + self.delta, seed_range.max + self.delta)
        if seed_range.min >= self.min and seed_range.max > self.max:
            return SeedRange(seed_range.min + self.delta, self.max + self.delta)

    def remainder_range(self, seed_range):
        if seed_range.min >= self.min and seed_range.max <= self.max:
            return None
        if seed_range.min < self.min and seed_range.max <= self.max:
            return SeedRange(seed_range.min, self.min - 1)
        if seed_range.min >= self.min and seed_range.max > self.max:
            return SeedRange(self.max + 1, seed_range.max)

class SeedRange:
    
    def __init__(self, start: int, end: int):
        self.min = start
        self.max = end
        
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
    seeds = [int(i) for i in lines[0].split(":")[1].split()]
    ranges = parse_ranges(lines[1:])
    part_1(seeds, ranges)
    seed_ranges = find_seed_ranges(seeds)
    part_2(seed_ranges, ranges)

def parse_ranges(lines: list):
    ranges = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.endswith("map:"):
            ranges.append([])
            continue
        values = line.split()
        new_range = TranslationRange(int(values[0]), int(values[1]), int(values[2]))
        ranges[-1].append(new_range)
    return ranges

def find_seed_ranges(seeds: list):
    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append(SeedRange(seeds[i], seeds[i] + seeds[i + 1] - 1))
    return seed_ranges

def part_1(initial_seeds: list, ranges: list):
    seeds = deepcopy(initial_seeds)
    for i in range(len(ranges)):
        for j in range(len(seeds)):
            for translation in ranges[i]:
                if translation.to_transform(seeds[j]):
                    seeds[j] = translation.transform(seeds[j])
                    break
    print(f"Part 1: {min(seeds)}")

def part_2(seed_ranges: list, ranges: list):
    working_set = deepcopy(seed_ranges)
    for i in range(len(ranges)):
        new_set = list()
        while working_set:
            curr = working_set.pop(0)
            translated = False
            for translation in ranges[i]:
                transformed = translation.transform_range(curr)
                if transformed:
                    translated = True
                    new_set.append(transformed)
                    remainder = translation.remainder_range(curr)
                    if remainder:
                        working_set.append(remainder)
                    break
            if not translated:
                new_set.append(curr)
        working_set = deepcopy(new_set)
    final_min = 100000000000000
    for final_range in working_set:
        if final_range.min < final_min:
            final_min = final_range.min
    print(f"Part 2: {final_min}")
      
if __name__ == "__main__":
    print(run_script("example.txt"))