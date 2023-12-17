import time
from typing import Union
from dataclasses import dataclass
from copy import deepcopy
import math

@dataclass
class Lens:
    label: str
    focal: int

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
    subparts = raw_data.split(",")
    part_1(subparts)
    part_2(subparts)

def part_1(subparts: list):
    values = []
    for string in subparts:
        values.append(get_val(string))
    print(f"Part 1: {sum(values)}")

def get_val(string: str):
    val = 0
    for c in string:
        val += ord(c)
        val *= 17
        val %= 256
    return val

def part_2(subparts: list):
    hashmap = []
    for i in range(256):
        hashmap.append([])
    for string in subparts:
        if "=" in string:
            curr_label, focal = string.split("=")
            focal = int(focal)
            box = get_val(curr_label)
            done = False
            for lens in hashmap[box]:
                if lens.label == curr_label:
                    lens.focal = focal
                    done = True
                    break
            if not done:
                hashmap[box].append(Lens(curr_label, focal))
        elif "-" in string:
            curr_label = string[:-1]
            box = get_val(curr_label)
            to_remove = None
            for i in range(len(hashmap[box])):
                if hashmap[box][i].label == curr_label:
                    to_remove = i
                    break
            if to_remove != None:
                del hashmap[box][to_remove]
        """
        print("After", string)
        for i in range(len(hashmap)):
            for j in range(len(hashmap[i])):
                label = hashmap[i][j].label
                focal = hashmap[i][j].focal
                print(i, j, label, focal)
        """
    total = 0
    for i in range(len(hashmap)):
        for j in range(len(hashmap[i])):
            label = hashmap[i][j].label
            focal = hashmap[i][j].focal
            print(i, j, label, focal)
            total += (i + 1) * (j + 1) * hashmap[i][j].focal
    print(f"Part 2: {total}")
    
if __name__ == "__main__":
    print(run_script("input.txt"))