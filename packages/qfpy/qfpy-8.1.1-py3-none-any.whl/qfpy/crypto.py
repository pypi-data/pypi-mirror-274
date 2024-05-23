"""
def caesar_encode(text: str, shift=3)

def get_md5_str(s: str)
"""

import hashlib
import string


def caesar_encode(text: str, shift=3):
    """
    凯撒编码
    编码和解码都用这个函数，只需要保证偏移相同

    shift: 偏移量，默认为 3
    """
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(shifted_alphabet, alphabet)
    return text.translate(table)


def get_md5_str(s: str):
    return hashlib.md5(s.encode()).hexdigest()
