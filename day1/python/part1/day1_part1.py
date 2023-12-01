#!/usr/bin/env python
# pylint: disable=missing-docstring
# pylint: disable=line-too-long

import functools

def readinput(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf-8') as fp:
        return fp.readlines()

def main():
    input_data = readinput('input2.txt')

    total = 0
    for line in input_data:
        nums = functools.reduce(lambda a, b: a+b, filter(lambda c: c in ['0,','1','2','3','4','5','6','7','8','9'], line))
        num = nums[0] + nums[-1]
        total += int(num)

        print(line)
        print(nums)
        print(num)
        print()

    print(f'Final value: {total}')

if __name__ == '__main__':
    main()
