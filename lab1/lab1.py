import sys

ROMANIAN_ALPHABET = 'AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ'
LATIN_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

MIN_KEYWORD_LENGTH = 7

# Cedilla variants (Ş, Ţ) typed on some keyboards are treated as the
# comma-below letters (Ș, Ț) required by the alphabet of the lab.
CEDILLA_TO_COMMA = str.maketrans({'\u015e': '\u0218', '\u0162': '\u021a'})


class CaesarCipher:

    def __init__(self, ordered_alphabet: str):
        self.alphabet = list(ordered_alphabet)
        self.N = len(self.alphabet)
        self.k = 0
        self.kw = []
        # Without a keyword the working alphabet is the natural one (Task 1.1)
        self.altered_alphabet = list(self.alphabet)
        self.altered_mapping = {l: i for i, l in enumerate(self.altered_alphabet)}

    # ---------- validation: every method returns an error message or None ----

    def check_k(self, k: int):
        if not 1 <= k <= self.N - 1:
            return f'Invalid key k = {k}. The key must be an integer between 1 and {self.N - 1} inclusive.'
        return None

    def check_text(self, text: str):
        for position, letter in enumerate(text, start=1):
            if letter not in self.alphabet:
                return (f"Invalid character '{letter}' at position {position}. "
                        f"Only letters of the Romanian alphabet (A-Z, Ă, Â, Î, Ș, Ț, "
                        f"uppercase or lowercase) and spaces are allowed.")
        if not text:
            return 'The text is empty. Enter at least one letter.'
        return None

    def check_keyword(self, keyword: str):
        if keyword == '':
            return None  # no keyword -> plain Caesar cipher (Task 1.1)
        for position, letter in enumerate(keyword, start=1):
            if letter not in self.alphabet:
                return (f"Invalid character '{letter}' at position {position} of the keyword. "
                        f"The keyword may contain only letters of the Romanian alphabet.")
        if len(keyword) < MIN_KEYWORD_LENGTH:
            return (f'The keyword is too short ({len(keyword)} characters). '
                    f'It must have at least {MIN_KEYWORD_LENGTH} characters.')
        return None

    # ---------- cipher parameters -------------------------------------------

    def set_cipher_params(self, k: int, keyword: str):
        self.k = k
        self.kw = unique_letters(keyword)
        self.set_keyword_params()

    def set_keyword_params(self):
        # keyword letters first (first occurrence only), then the remaining
        # letters of the alphabet in their natural order
        self.altered_alphabet = self.kw + [l for l in self.alphabet if l not in self.kw]
        self.altered_mapping = {l: i for i, l in enumerate(self.altered_alphabet)}

    # ---------- encryption / decryption -------------------------------------

    def shift_indexes(self, indexes: list[int], k: int) -> list[int]:
        # Python's % already returns a value in 0..N-1 for negative numbers
        return [(i + k) % self.N for i in indexes]

    def cipher(self, message: str) -> str:
        message_indexes = [self.altered_mapping[l] for l in message]
        shifted_indexes = self.shift_indexes(message_indexes, self.k)
        return ''.join(self.altered_alphabet[i] for i in shifted_indexes)

    def decipher(self, cipher: str) -> str:
        cipher_indexes = [self.altered_mapping[l] for l in cipher]
        shifted_indexes = self.shift_indexes(cipher_indexes, -self.k)
        return ''.join(self.altered_alphabet[i] for i in shifted_indexes)


def unique_letters(text: str) -> list[str]:
    # keeps only the first occurrence of every letter, in order of appearance
    return list(dict.fromkeys(text))


def format_text(text: str) -> str:
    return text.upper().translate(CEDILLA_TO_COMMA).replace(' ', '')


def ask(prompt: str, convert, check):
    """Asks for a value until it is valid; prints the reason on every failure."""
    while True:
        raw = input(prompt)
        try:
            value = convert(raw)
        except ValueError:
            print(f"Invalid input '{raw}'. An integer is expected.")
            continue
        error = check(value)
        if error is None:
            return value
        print(error)


if __name__ == "__main__":
    cipherer = CaesarCipher(ROMANIAN_ALPHABET)
    input_option = ask('Enter option (1 - encryption, 2 - decryption): ', int,
                       lambda o: None if o in (1, 2) else 'Invalid option. Enter 1 or 2.')
    input_k = ask(f'Enter key k (1-{cipherer.N - 1}): ', int, cipherer.check_k)
    input_kw = ask(f'Enter keyword (at least {MIN_KEYWORD_LENGTH} letters, blank if not used): ',
                   format_text, cipherer.check_keyword)
    input_text = ask('Enter message: ', format_text, cipherer.check_text)

    cipherer.set_cipher_params(input_k, input_kw)
    print('Alphabet used:', ' '.join(cipherer.altered_alphabet))
    if input_option == 1:
        print('Ciphertext:', cipherer.cipher(input_text))
    else:
        print('Plaintext: ', cipherer.decipher(input_text))
