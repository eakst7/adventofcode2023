#!/usr/bin/env python

from day7_part2 import process, HandClass, evaluate_hand, str_to_hand, generate_pseudo_hands

def test():
    assert process('./day7/python/part2/input1.txt') == 5905

def test_generate_pseudo_hands():
    assert generate_pseudo_hands(str_to_hand('TJJQK')) == [[10,10,10,12,13],[10,12,12,12,13],[10,13,13,12,13]]
    assert generate_pseudo_hands(str_to_hand('JJJJJ')) == [[13,13,13,13,13]]

def test_str_to_hand():
    assert str_to_hand('AKQJT') == [14,13,12,1,10]
    assert str_to_hand('9KQA2') == [9,13,12,14,2]

def test_evaluate_str():
    assert evaluate_hand(str_to_hand('A2256')) == HandClass.ONE_PAIR
    assert evaluate_hand(str_to_hand('A2233')) == HandClass.TWO_PAIR
    assert evaluate_hand(str_to_hand('23233')) == HandClass.FH
    assert evaluate_hand(str_to_hand('32322')) == HandClass.FH
    assert evaluate_hand(str_to_hand('1234A')) == HandClass.HIGH


def test_evaluate():
    assert evaluate_hand([1,1,1,1,1]) == HandClass.FIVE
    
    assert evaluate_hand([1,1,1,1,2]) == HandClass.FOUR
    assert evaluate_hand([1,1,1,2,1]) == HandClass.FOUR
    assert evaluate_hand([1,1,2,1,1]) == HandClass.FOUR
    assert evaluate_hand([1,2,1,1,1]) == HandClass.FOUR
    assert evaluate_hand([2,1,1,1,1]) == HandClass.FOUR

    assert evaluate_hand([3,3,3,3,2]) == HandClass.FOUR
    assert evaluate_hand([3,3,3,2,3]) == HandClass.FOUR
    assert evaluate_hand([3,3,2,3,3]) == HandClass.FOUR
    assert evaluate_hand([3,2,3,3,3]) == HandClass.FOUR
    assert evaluate_hand([2,3,3,3,3]) == HandClass.FOUR

    assert evaluate_hand([1,1,1,2,2]) == HandClass.FH
    assert evaluate_hand([1,1,2,2,1]) == HandClass.FH
    assert evaluate_hand([1,2,2,1,1]) == HandClass.FH
    assert evaluate_hand([2,2,1,1,1]) == HandClass.FH
    assert evaluate_hand([1,2,1,2,1]) == HandClass.FH
    assert evaluate_hand([1,2,2,1,1]) == HandClass.FH

    assert evaluate_hand([3,3,3,2,2]) == HandClass.FH
    assert evaluate_hand([3,3,2,2,3]) == HandClass.FH
    assert evaluate_hand([3,2,2,3,3]) == HandClass.FH
    assert evaluate_hand([2,2,3,3,3]) == HandClass.FH
    assert evaluate_hand([3,2,3,2,3]) == HandClass.FH
    assert evaluate_hand([3,2,2,3,3]) == HandClass.FH

    assert evaluate_hand([1,1,1,2,3]) == HandClass.THREE

    assert evaluate_hand([1,1,2,3,3]) == HandClass.TWO_PAIR
    assert evaluate_hand([1,1,3,2,3]) == HandClass.TWO_PAIR

    assert evaluate_hand([1,1,2,3,4]) == HandClass.ONE_PAIR
    assert evaluate_hand([1,2,2,3,4]) == HandClass.ONE_PAIR
    assert evaluate_hand([1,2,3,3,4]) == HandClass.ONE_PAIR
    assert evaluate_hand([1,2,3,4,4]) == HandClass.ONE_PAIR

    assert evaluate_hand([1,2,3,4,5]) == HandClass.HIGH
