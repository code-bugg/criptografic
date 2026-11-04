#!/usr/bin/env python3
"""Lab 3, Task 3.1 -- Playfair cipher over the Romanian alphabet (31 letters)."""

import re

# Romanian alphabet: 31 letters.
RO_ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"

# 31 is prime, so it cannot fill a rectangular matrix. Following the handout
# (drop the rarest letter), Q is merged with K -> 30 symbols -> 5x6 matrix.
MERGE = {"Q": "K"}
ROWS, COLS = 5, 6
MATRIX_ALPHABET = "".join(c for c in RO_ALPHABET if c not in MERGE)

FILLER, FILLER_ALT = "X", "Z"      # rare letters used as padding
MIN_KEY_LEN = 7
VALID_TEXT = re.compile(r"[A-Za-z]+")


def normalize(text, alphabet=MATRIX_ALPHABET, merge=MERGE):
    """Upper-case the text and apply the letter merges (Q -> K)."""
    text = "".join(text.split()).upper()
    return "".join(merge.get(c, c) for c in text)


def validate_plain(text):
    """Plaintext/key: only A-Z, a-z (spaces are removed first)."""
    compact = "".join(text.split())
    if not compact or not VALID_TEXT.fullmatch(compact):
        raise ValueError("Only the Latin letters 'A'-'Z' and 'a'-'z' are "
                         "allowed (spaces are ignored). Remove digits, "
                         "punctuation and diacritics.")
    return compact


def validate_cipher(text):
    """Ciphertext may also contain Ă Â Î Ș Ț (they sit in the matrix)."""
    compact = "".join(text.split()).upper()
    if not compact or any(c not in MATRIX_ALPHABET for c in compact):
        raise ValueError("The ciphertext may contain only letters of the "
                         "Romanian alphabet ('A'-'Z', 'a'-'z', Ă, Â, Î, Ș, "
                         "Ț), without 'Q'.")
    return compact


def build_matrix(key, alphabet=MATRIX_ALPHABET, cols=COLS):
    """Key without repeated letters first, then the rest of the alphabet."""
    seen = []
    for c in normalize(key) + alphabet:
        if c in alphabet and c not in seen:
            seen.append(c)
    return [seen[i:i + cols] for i in range(0, len(seen), cols)]


def prepare(text):
    """Split into digraphs; insert a filler between equal letters and
    pad an odd-length text with a filler."""
    pairs, i = [], 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else None
        if b is None or a == b:
            pairs.append(a + (FILLER if a != FILLER else FILLER_ALT))
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    return pairs


def _positions(matrix):
    return {c: (r, k) for r, row in enumerate(matrix) for k, c in enumerate(row)}


def _transform(pairs, matrix, step):
    """step = +1 encrypts, step = -1 decrypts."""
    pos = _positions(matrix)
    rows, cols = len(matrix), len(matrix[0])
    out = []
    for a, b in pairs:
        (r1, c1), (r2, c2) = pos[a], pos[b]
        if r1 == r2:                                   # same row
            out.append(matrix[r1][(c1 + step) % cols] +
                       matrix[r2][(c2 + step) % cols])
        elif c1 == c2:                                 # same column
            out.append(matrix[(r1 + step) % rows][c1] +
                       matrix[(r2 + step) % rows][c2])
        else:                                          # rectangle
            out.append(matrix[r1][c2] + matrix[r2][c1])
    return out


def encrypt(message, key):
    matrix = build_matrix(key)
    pairs = prepare(normalize(message))
    return "".join(_transform(pairs, matrix, +1))


def decrypt(cipher, key):
    matrix = build_matrix(key)
    text = normalize(cipher)
    pairs = [text[i:i + 2] for i in range(0, len(text), 2)]
    return "".join(_transform(pairs, matrix, -1))


def show(matrix):
    return "\n".join(" ".join(row) for row in matrix)


def read_key():
    while True:
        try:
            key = validate_plain(input("Key (min. %d letters): " % MIN_KEY_LEN))
        except ValueError as e:
            print("  Error:", e)
            continue
        if len(key) < MIN_KEY_LEN:
            print("  Error: the key must have at least %d letters." % MIN_KEY_LEN)
            continue
        return key


def main():
    while True:
        op = input("Operation [1 = encrypt, 2 = decrypt, 0 = exit]: ").strip()
        if op == "0":
            break
        if op not in ("1", "2"):
            print("  Error: choose 1, 2 or 0.")
            continue
        key = read_key()
        print("Matrix:\n" + show(build_matrix(key)))
        while True:
            try:
                if op == "1":
                    msg = validate_plain(input("Message: "))
                    print("Ciphertext:", encrypt(msg, key))
                else:
                    msg = validate_cipher(input("Ciphertext: "))
                    if len(msg) % 2:
                        raise ValueError("The ciphertext must have an even "
                                         "number of letters.")
                    print("Decrypted text:", decrypt(msg, key))
                break
            except ValueError as e:
                print("  Error:", e)


if __name__ == "__main__":
    main()
