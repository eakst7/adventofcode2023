#!/usr/bin/env python
# pylint: disable=missing-docstring
# pylint: disable=line-too-long

def read_input(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf-8') as fp:
        return fp.readlines()

def main():
    input_data = read_input('input2.txt')

    total = 0
    for line in input_data:
        print(f"{line=}")
        (gameid,rounds) = line.split(':')
        gameid = int(gameid.split(' ')[1])
        print(f"ID: {gameid}")
        print(f"{rounds}")
        rounds = rounds.split(';')

        minred = 0
        mingreen = 0
        minblue = 0

        for rnd in rounds:
            print(f"{rnd}")

            redcount = 0
            greencount = 0
            bluecount = 0

            balls = rnd.split(',')
            for b in balls:
                b = b.strip()

                if b.endswith('blue'):
                    bluecount = int(b.split(' ')[0])
                if b.endswith('red'):
                    redcount = int(b.split(' ')[0])
                if b.endswith('green'):
                    greencount = int(b.split(' ')[0])

            print(f"({redcount},{greencount},{bluecount})")

            minred = max(minred, redcount)
            mingreen = max(mingreen, greencount)
            minblue = max(minblue, bluecount)

        game_power = minred * mingreen * minblue

        total += game_power


    print(f"{total=}")
              

if __name__ == '__main__':
    main()