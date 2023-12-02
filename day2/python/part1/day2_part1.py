#!/usr/bin/env python
# pylint: disable=missing-docstring
# pylint: disable=line-too-long

input_data = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''.split('\n')

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

        round_ok = True
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
            if (redcount > 12) or (greencount > 13) or (bluecount > 14):
                print(f"Game {gameid} is not possible")
                round_ok = False
                break
        if round_ok:
            total += gameid


    print(f"{total=}")

                

if __name__ == '__main__':
    main()