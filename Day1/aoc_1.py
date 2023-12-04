import time
from typing import Union

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
    part_2(lines)
    return 0

def part_1(lines: list) -> None:
    total = 0
    for line in lines:
        current = ""
        for i in range(len(line)):
            if line[i].isnumeric():
                current += line[i]
                break
        for i in range(len(line) - 1, -1, -1):
            if line[i].isnumeric():
                current += line[i]
                break
        total += int(current)
    print(f"Part 1: {total}")

def part_2(lines: list) -> None:
    total = 0
    for line in lines:
        current = 0
        for i in range(len(line)):
            val = check(line, i)
            if val == -1:
                continue
            current += val * 10
            break
        for i in range(len(line) - 1, -1, -1):
            val = check(line, i)
            if val == -1:
                continue
            current += val
            break
        total += current
    print(f"Part 2: {total}")

def check(line: str, idx: int) -> int:
    if line[idx] == "o":
        if line[idx:idx+3] == "one":
            return 1
    if line[idx] == "t":
        if line[idx:idx+3] == "two":
            return 2
        if line[idx:idx+5] == "three":
            return 3
    if line[idx] == "f":
        if line[idx:idx+4] == "four":
            return 4
        if line[idx:idx+4] == "five":
            return 5
    if line[idx] == "s":
        if line[idx:idx+3] == "six":
            return 6
        if line[idx:idx+5] == "seven":
            return 7
    if line[idx] == "e":
        if line[idx:idx+5] == "eight":
            return 8
    if line[idx] == "n":
        if line[idx:idx+4] == "nine":
            return 9
    if line[idx].isnumeric():
        return int(line[idx])
    return -1
    
if __name__ == "__main__":
    print(run_script("example2.txt"))