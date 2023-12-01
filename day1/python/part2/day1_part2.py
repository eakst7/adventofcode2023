#!/usr/bin/env python
# pylint: disable=missing-docstring
# pylint: disable=line-too-long
import re

def readinput(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf-8') as fp:
        return fp.readlines()


def main():
    input_data = readinput('input2.txt')

    total = 0
    for line in input_data:
        first = findfirst(line)
        last = findlast(line)
        num = str_to_digit(first) + str_to_digit(last)
        total += int(num)

        print(f"{num} {total} {line.strip()}")

    print(f'Final value: {total}')

def str_to_digit(strnum: str) -> str:
    match strnum:
        case 'one':
            return '1'
        case 'two':
            return '2'
        case 'three':
            return '3'
        case 'four':
            return '4'
        case 'five':
            return '5'
        case 'six':
            return '6'
        case 'seven':
            return '7'
        case 'eight':
            return '8'
        case 'nine':
            return '9'
        case 'zero':
            return '0'
        case _:
            return strnum

def findfirst(line: str) -> str:
    for i in range(0,len(line)):
        m = re.search(r'1|2|3|4|5|6|7|8|9|0|one|two|three|four|five|six|seven|eight|nine|zero', line[:i])
        if m is not None:
            return m.group(0)

def findlast(line: str) -> str:
    for i in range(1,len(line)+1):
        x = len(line) - i
        m = re.search(r'1|2|3|4|5|6|7|8|9|0|one|two|three|four|five|six|seven|eight|nine|zero', line[x:])
        if m is not None:
            return m.group(0)

if __name__ == '__main__':
    main()
