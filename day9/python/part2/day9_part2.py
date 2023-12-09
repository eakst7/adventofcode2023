#!/usr/bin/env python3
input_data: str

def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read()

def calc1(input: list[int]) -> list[int]:
    out = []
    for i in range(1,len(input)):
        out.append(input[i] - input[i-1])
    print(out)
    return out

def allsame(input: list[int]) -> bool:
    for i in range(1,len(input)):
        if input[i] != input[i-1]:
            return False
        
    return True

def calc2(input: list[int]) -> int:
    if (allsame(input)):
        return input[-1]
    else:
        return input[0] - calc2(calc1(input))

def process(filename: str) -> int:
    readinput(filename)
    total: int = 0

    for line in input_data.split("\n"):
        sequence = [int(x) for x in line.split(" ")]
        print(sequence)
        v = calc2(sequence)
        total += v
        print(f"{v=} {total=}")

    print(f"{total=}")
    return total

if __name__ == "__main__":
    process("input2.txt")
