#!/usr/bin/env python3
"""Lab 4, Task 2.4 -- DES: given an 8-character message, find L1.

L1 = R0, where (L0, R0) = IP(M) is the split of the initial permutation.
"""

import random
import string

IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]


def to_bits(text):
    """8 ASCII characters -> 64-bit string (8 bits per character)."""
    return "".join(format(ord(c), "08b") for c in text)


def group(bits, n=8):
    return " ".join(bits[i:i + n] for i in range(0, len(bits), n))


def permute(bits, table):
    return "".join(bits[i - 1] for i in table)


def to_hex(bits):
    return format(int(bits, 2), "0%dX" % (len(bits) // 4))


def validate(text):
    if len(text) != 8:
        raise ValueError("The message must have exactly 8 characters "
                         "(now %d)." % len(text))
    if any(ord(c) > 127 for c in text):
        raise ValueError("Only ASCII characters (code 0-127) are allowed.")
    return text


def print_table(title, table, cols=8):
    print(title)
    for i in range(0, len(table), cols):
        print("  " + " ".join("%2d" % x for x in table[i:i + cols]))


def l1_of_block(text, verbose=True):
    bits = to_bits(text)
    ip = permute(bits, IP)
    l0, r0 = ip[:32], ip[32:]
    l1 = r0
    if verbose:
        print("Message M      :", text)
        print("ASCII codes    :", " ".join("%3d" % ord(c) for c in text))
        print("Hex            :", to_hex(bits))
        print("M (64 bits)    :", group(bits))
        print_table("Initial permutation IP:", IP)
        print("IP(M)          :", group(ip))
        print("L0 (32 bits)   :", group(l0))
        print("R0 (32 bits)   :", group(r0))
        print("L1 = R0        :", group(l1), " (hex %s)" % to_hex(l1))
    return l1


def main():
    while True:
        choice = input("1 = enter message, 2 = random message, 0 = exit: ").strip()
        if choice == "0":
            break
        if choice == "2":
            text = "".join(random.choice(string.ascii_letters + string.digits)
                           for _ in range(8))
        elif choice == "1":
            text = input("Message (8 characters): ")
            try:
                validate(text)
            except ValueError as e:
                print("  Error:", e)
                continue
        else:
            print("  Error: choose 1, 2 or 0.")
            continue
        l1_of_block(text)


if __name__ == "__main__":
    main()
