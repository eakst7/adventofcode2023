#!/usr/bin/env python3
from enum import Enum
from functools import cmp_to_key


input_data: str

class HandClass(Enum):
    FIVE = 7
    FOUR = 6
    FH = 5
    THREE = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH = 1

type Card = int
type Hand = list[Card]

def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read()

def generate_pseudo_hands(hand: Hand) -> list[Hand]:
    if 1 not in hand:
        return [hand]
    
    if sum(hand) == 5:
        return [[13, 13, 13, 13, 13]]

    pseudo_hands = []
    for c in hand:
        if c == 1: continue
        nexthand = []
        for c2 in hand:
            if c2 == 1:
                nexthand.append(c)
            else:
                nexthand.append(c2)
        pseudo_hands.append(nexthand)

    return pseudo_hands
        

def str_to_hand(input: str) -> Hand:
    h: Hand = []
    for c in input:
        match c:
            case 'A':
                h.append(14)
                continue
            case 'K':
                h.append(13)
                continue
            case 'Q':
                h.append(12)
                continue
            case 'J':
                h.append(1)
                continue
            case 'T':
                h.append(10)
                continue
            case _:
                h.append(int(c))
    return h

def has_three(hand: Hand) -> int:
    # returns the position of the first of the three of a kind
    # The hand is sorted
    # 11123 hand[0] == hand[2]
    # 12223 hand[1] == hand[3]
    # 12333 hand[2] == hand[4]
    if hand[0] == hand[2]: return 0
    if hand[1] == hand[3]: return 1
    if hand[2] == hand[4]: return 2
    return -1
        
def has_four(hand: Hand) -> bool:
    # 11112 hand[0] == hand[3]
    # 12222 hand[1] == hand[4]
    return hand[0] == hand[3] or \
           hand[1] == hand[4]

def has_five(hand: Hand) -> bool:
    return hand[0] == hand[4]

def has_fh(hand: Hand, three_of_a_kind_pos: int) -> bool:
    # already known to have three
    # 11122
    # 11222
    if three_of_a_kind_pos == 0:  # t.o.k. at the beginning, check last two
        return hand[3] == hand[4]
    if three_of_a_kind_pos == 2:  # t.o.k. at then end, check first two
        return hand[0] == hand[1]
    
    return False

def has_one_pair(hand: Hand) -> int:
    # returns the position of the first of the pair
    # 11234
    # 12234
    # 12334
    # 12344
    if hand[0] == hand[1]: return 0
    if hand[1] == hand[2]: return 1
    if hand[2] == hand[3]: return 2
    if hand[3] == hand[4]: return 3

    return -1

def has_two_pair(hand: Hand, first_pair_pos: int) -> bool:
    # 11223
    # 11233
    # 12233
    if first_pair_pos == 0:  # xx112, xx122
        return \
            hand[2] == hand[3] or \
            hand[3] == hand[4]
    if first_pair_pos == 1:  # 1xx22
        return \
            hand[3] == hand[4]
    
    return False

def evaluate_hand(hand: Hand) -> HandClass:
    sorted_hand = sorted(hand)
    tok_pos = has_three(sorted_hand)
    if tok_pos >= 0:
        if has_four(sorted_hand):
            if has_five(sorted_hand):
                return HandClass.FIVE
            return HandClass.FOUR
        if has_fh(sorted_hand, tok_pos):
            return HandClass.FH
        return HandClass.THREE
    
    pair_pos = has_one_pair(sorted_hand)
    if pair_pos >= 0:
        if has_two_pair(sorted_hand, pair_pos):
            return HandClass.TWO_PAIR
        return HandClass.ONE_PAIR
    
    return HandClass.HIGH

def evaluate_hand_group(hand: Hand) -> HandClass:
    pseudo_hands = generate_pseudo_hands(hand)

    pseudo_hand_classes = []
    for hand in pseudo_hands:
        pseudo_hand_classes.append(evaluate_hand(hand))

    print(f"{hand=}")
    print(f"{pseudo_hand_classes=}")

    return sorted(pseudo_hand_classes, key=cmp_to_key(hand_class_sort))[-1]


def process(filename: str) -> int:
    readinput(filename)
    total: int = 0

    all_hands: list[tuple[Hand, int, HandClass]] = []
    for line in input_data.split('\n'):
        (cards, bid) = line.split(' ')

        hand = str_to_hand(cards)
        hand_class = evaluate_hand_group(hand)

        all_hands.append( (hand, int(bid), hand_class) )

    sorted_hands = sorted(all_hands, key=cmp_to_key(hand_sort))
    for rank,h in enumerate(sorted_hands):
        print(f"{rank}: {h}")
        bid = h[1]
        total += (rank+1) * h[1]

    print(f"{total=}")
    return total

def hand_class_sort(h1: HandClass, h2: HandClass) -> int:
    if h1.value > h2.value:
        return 1
    if h1.value < h2.value:
        return -1
    
    return 0


def hand_sort(h1: tuple[Hand, int, HandClass], h2: tuple[Hand, int, HandClass]) -> int:
    h1_class = h1[2]
    h2_class = h2[2]

    if h1_class.value > h2_class.value:
        return 1
    if h1_class.value < h2_class.value:
        return -1
    
    h1_hand = h1[0]
    h2_hand = h2[0]
    for i in range(len(h1_hand)):
        if h1_hand[i] > h2_hand[i]:
            return 1
        if h1_hand[i] < h2_hand[i]:
            return -1
        
    return 0

if __name__ == "__main__":
    process("input2.txt")
