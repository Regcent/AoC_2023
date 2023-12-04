import time
from typing import Union
from dataclasses import dataclass
from copy import deepcopy

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
    cards = parse_cards(lines)
    count_winning_numbers(cards)
    part_1(cards)
    part_2(cards)

def parse_cards(lines: list):
    cards = {"win": [], "own": []}
    for line in lines:
        numbers = line.split(":")[1]
        win_raw, own_raw = numbers.split("|")
        cards["win"].append([int(i) for i in win_raw.split()])
        cards["own"].append([int(i) for i in own_raw.split()])
    return cards

def count_winning_numbers(cards):
    cards["points"] = []
    for i in range(len(cards["own"])):
        sub = 0
        for number in cards["win"][i]:
            if number in cards["own"][i]:
                sub += 1
        cards["points"].append(sub)

def part_1(cards):
    total = 0
    for i in range(len(cards["points"])):
        sub = cards["points"][i]
        total += 0 if sub == 0 else 2 ** (sub - 1)
    print(f"Part 1: {total}")

def part_2(cards):
    copies = [1] * len(cards["own"])
    idx = 0
    while idx < len(copies):
        won_cards = cards["points"][idx]
        for i in range(idx + 1, min(len(copies), idx + won_cards + 1)):
            copies[i] += copies[idx]
        idx += 1
    print(f"Part 2: {sum(copies)}")
      
if __name__ == "__main__":
    print(run_script("input.txt"))