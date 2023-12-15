#!/usr/bin/env python3
from dataclasses import dataclass
from icecream import ic
import re
input_data: str

def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read()

def hash(s: str) -> int:
    current_value = 0
    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value


@dataclass
class Lens:
    label: str
    focal_length: int

boxes: dict[int,list[Lens]] = {}

def add_lens(boxnum: int, label: str, value: int):
    global boxes
    if boxes.get(boxnum) is None:
        boxes[boxnum] = []

    for lens in boxes[boxnum]:
        if lens.label == label:
            lens.focal_length = value
            return
        
    boxes[boxnum].append(Lens(label, value))

def remove_lens(boxnum: int, label: str):
    global boxes
    if boxes.get(boxnum) is None:
        return
    
    remove = -1
    lens_list = boxes[boxnum]
    for (i,lens) in enumerate(lens_list):
        if lens.label == label:
            remove = i
            break

    if remove >= 0:
        del lens_list[remove]

def process(filename: str) -> int:
    readinput(filename)
    total: int = 0

    steps = input_data.split(",")

    for (i,step) in enumerate(steps):
        ic(i, len(steps))
        (label, op, value) = re.split("(=|-)", step)
        box = hash(label)
        match op:
            case "=":
                add_lens(box, label, int(value))
            case "-":
                remove_lens(box, label)

        #ic(boxes)

    for boxnum in range(0,256):
        if boxes.get(boxnum) is None:
            continue
        for (slot,lens) in enumerate(boxes[boxnum]):
            total += (boxnum+1) * (slot+1) * lens.focal_length


    print(f"{total=}")
    return total

if __name__ == "__main__":
    process("input2.txt")
