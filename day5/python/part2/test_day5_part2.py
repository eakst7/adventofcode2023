#!/usr/bin/env python

from day5_part2 import process, CompressedMap


def test():
    assert process('./day5/python/part2/input1.txt') == 46

def test_cm():
    cm = CompressedMap()
    cm.add_range(910271444,3030771176,70771974)

    assert cm.get(1) == 1

    assert cm.get(3030771176) == 910271444

def test_cm2():
    cm = CompressedMap()
    cm.add_range(50,98,2)
    cm.add_range(52,50,48)

    assert cm.get2(51,3) == (53,3)
    assert cm.get2(1,10) == (1, 10)
    assert cm.get2(98, 4) == (50, 2)

    assert cm.get2(96, 4) == (98, 2)
    assert cm.get2(98, 2) == (50, 2)

    assert cm.get2(50,1) == (52, 1)
    assert cm.get2(45, 10) == (45, 5)

def test_cm3():
    cm = CompressedMap()
    cm.add_range(50,98,2)
    cm.add_range(52,50,48)

    l = []

    src = 96
    srclen = 4

    done = False
    while not done:
        (out, outlen) = cm.get2(src, srclen)
        print(f"{out}/{outlen}")
        l.append((out,outlen))
        if (srclen == outlen):
            done = True
        else:
            src = src + outlen
            srclen = srclen - outlen

    assert cm.get2(98, 4) == (50, 2)

def test_x():
    cm = CompressedMap()
    cm.add_range(50,98,2)
    cm.add_range(52,50,48)
    cm.add_range(10, 7, 5)

    l = []

def test_before_first_range():
    cm = CompressedMap()
    cm.add_range(50,98,2)
    cm.add_range(52,50,48)

    assert cm.get2(10,12) == (10, 12)
    assert cm.get2(0,12) == (0, 12)

def test_after_last_range():
    cm = CompressedMap()
    cm.add_range(50,98,2)
    cm.add_range(52,50,48)

    assert cm.get2(100,12) == (100, 12)
    assert cm.get2(124,12) == (124, 12)

def test_in_first_range():
    cm = CompressedMap()
    cm.add_range(50,98,2)
    cm.add_range(52,50,48)

    assert cm.get2(50,5) == (52, 5)
    assert cm.get2(55,5) == (57, 5)

def test_in_second_range():
    cm = CompressedMap()
    cm.add_range(50,98,2)
    cm.add_range(52,50,48)

    assert cm.get2(98,2) == (50, 2)
    assert cm.get2(99,1) == (51, 1)

def test_in_before_and_into_first_range():
    cm = CompressedMap()
    cm.add_range(50,98,2)
    cm.add_range(52,50,48)

    assert cm.get2(45,10) == (45, 5)
    assert cm.get2(50,5) == (52, 5)

def test_in_before_and_through_first_range():
    cm = CompressedMap()
    cm.add_range(50,98,2)
    cm.add_range(52,50,48)

    assert cm.get2(45,200) == (45, 5)

def test_in_and_after_first_range():
    cm = CompressedMap()
    cm.add_range(50,98,2)
    cm.add_range(52,50,20)

    assert cm.get2(55,20) == (57, 15)

def test_between_first_and_second_range():
    cm = CompressedMap()
    cm.add_range(50,98,2)
    cm.add_range(52,50,20)

    assert cm.get2(75,20) == (75, 20)

def test_between_first_and_after_second_range():
    cm = CompressedMap()
    cm.add_range(50,98,2)
    cm.add_range(52,50,20)

    assert cm.get2(45,100) == (45, 5)
    assert cm.get2(50,96) == (52, 20)

def test_z():
    cm = CompressedMap()
    cm.add_range(2,5,2)
    cm.add_range(6,8,2)

    r = cm.get2(0,12)

    r = cm.getall(0,12)

    assert r == [(0,5),(2,2),(7,1),(6,2),(10,2)]
    print(f"{r=}")

    #(0,5)(2,2)(7,1)(6,2)(10,2)
def test_a():
    cm = CompressedMap()
    cm.add_range(2,5,2)
    cm.add_range(6,8,2)

    r = cm.get2(0,12)

    r = cm.getall2([(0,12),(13,5)])

    assert r == [(0,5),(2,2),(7,1),(6,2),(10,2),(13,5)]
    print(f"{r=}")