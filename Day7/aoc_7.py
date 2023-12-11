import time
from typing import Union
from dataclasses import dataclass
from copy import deepcopy
import functools

REFERENCE_1 = "23456789TJQKA"
REFERENCE_2 = "J23456789TQKA"
FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

class CamelHand:

    def __init__(self, hand: str, bid: int, value_function, ref: str):
        self.bid = bid
        values = {}
        for char in hand:
            if char not in values:
                values[char] = hand.count(char)
        self.hand_value = value_function(values)
        self.hand_raw = [ref.index(c) for c in hand]
        self.hand = hand

    def __lt__(self, other):
        if self.hand_value < other.hand_value:
            return True
        if self.hand_value > other.hand_value:
            return False
        for i in range(len(self.hand_raw)):
            if self.hand_raw[i] < other.hand_raw[i]:
                return True
            if self.hand_raw[i] > other.hand_raw[i]:
                return False

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

def part_1(lines: list):
    hands = []
    for line in lines:
        hand, bid = line.split()
        hands.append(CamelHand(hand, int(bid), find_camel_value, REFERENCE_1))
    hands.sort()
    total = 0
    for i in range(len(hands)):
        total += hands[i].bid * (i + 1)
    print(f"Part 1: {total}")
    
def find_camel_value(values: dict):
    if len(values) == 1:
        return FIVE_OF_A_KIND
    elif len(values) == 2:
        for key in values:
            if values[key] == 4:
                return FOUR_OF_A_KIND
        return FULL_HOUSE
    elif len(values) == 3:
        for key in values:
            if values[key] == 3:
                return THREE_OF_A_KIND
        return TWO_PAIR
    elif len(values) == 4:
        return ONE_PAIR
    else:
        return HIGH_CARD

def part_2(lines: list):
    hands = []
    for line in lines:
        hand, bid = line.split()
        hands.append(CamelHand(hand, int(bid), optimize_camel_value, REFERENCE_2))
    hands.sort()
    total = 0
    for i in range(len(hands)):
        print(hands[i].hand)
        total += hands[i].bid * (i + 1)
    print(f"Part 2: {total}")
    
def optimize_camel_value(values: dict):
    if "J" not in values:
        return find_camel_value(values)
    if len(values) <= 2:
        return FIVE_OF_A_KIND
    if len(values) == 3:
        if values["J"] == 1:
            for key in values:
                if values[key] == 2:
                    return FULL_HOUSE
        return FOUR_OF_A_KIND
    if len(values) == 4:
        return THREE_OF_A_KIND
    if len(values) == 5:
        return ONE_PAIR

if __name__ == "__main__":
    print(run_script("input.txt"))