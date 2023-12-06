#!/usr/bin/env python3

# Sample
#input_data = [(7,9), (15,40), (30,200)]

# Part 1
#input_data: list[tuple[int,int]]= [(40,219), (81,1012), (77,1365), (72,1089)]

# Part 2
input_data: list[tuple[int,int]]= [(40817772,219101213651089)]

# Time:        40     81     77     72
# Distance:   219   1012   1365   1089

# def readinput(filename: str):
#     global input_data
#     with open(filename, "r", encoding="utf-8") as fp:
#         input_data = fp.read(filename)


def process(input_data: list[tuple[int,int]]) -> int:
    total = 1
    for (t,d) in input_data:
        total *= count_winners(t,d)

    print(f"{total=}")
    return total

def calc_speed(charge_time: int) -> int:
    return charge_time

def calc_distance(speed: int, run_time: int) -> int:
    return speed * run_time

def count_winners(race_duration: int, distance_to_beat: int) -> int:
    
    count = 0
    for t in range(race_duration):
        dist = calc_distance(calc_speed(t), race_duration-t)
        if dist > distance_to_beat:
            count += 1

    return count

if __name__ == "__main__":
    process(input_data)
    

