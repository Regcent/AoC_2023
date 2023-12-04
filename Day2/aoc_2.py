import time
from typing import Union
from dataclasses import dataclass

@dataclass
class CubeSet:
    red: int
    green: int
    blue: int

    def __str__(self) -> str:
        return f"Red: {self.red}, Blue: {self.blue}, Green: {self.green}"

@dataclass
class Game:
    cube_sets: list

    def __str__(self) -> str:
        return ";".join([str(cube_set) for cube_set in self.cube_sets])

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
    games = parse_games(lines)
    part_1(games)
    part_2(games)
    return 0

def parse_games(lines: list) -> list:
    games = []
    for i in range(len(lines)):
        sets = lines[i].split(":")[1].split(";")
        game = Game([])
        for cubes in sets:
            elems = cubes.split(",")
            cube_set = CubeSet(0, 0, 0)
            for elem in elems:
                sub_parts = elem.split()
                number = int(sub_parts[0])
                if sub_parts[1].startswith("g"):
                    cube_set.green = number
                if sub_parts[1].startswith("r"):
                    cube_set.red = number
                if sub_parts[1].startswith("b"):
                    cube_set.blue = number
            game.cube_sets.append(cube_set)
        games.append(game)
    return games

def part_1(games: list) -> None:
    total = 0
    MAX_RED = 12
    MAX_GREEN = 13
    MAX_BLUE = 14
    valid = True
    for i in range(len(games)):
        for cube_set in games[i].cube_sets:
            valid = cube_set.blue <= MAX_BLUE
            if not valid:
                break
            valid = cube_set.red <= MAX_RED
            if not valid:
                break
            valid = cube_set.green <= MAX_GREEN
            if not valid:
                break
        if valid:
            total += i + 1
    print(f"Part 1: {total}")

def part_2(games: list) -> None:
    total = 0
    for game in games:
        min_red = 0
        min_blue = 0
        min_green = 0
        for cube_set in game.cube_sets:
            if cube_set.green > min_green:
                min_green = cube_set.green
            if cube_set.blue > min_blue:
                min_blue = cube_set.blue
            if cube_set.red > min_red:
                min_red = cube_set.red
        total += min_red * min_blue * min_green
    print(f"Part 2: {total}")

if __name__ == "__main__":
    print(run_script("input.txt"))