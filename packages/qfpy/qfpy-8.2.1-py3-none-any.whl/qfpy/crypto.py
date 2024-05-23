"""
def caesar_encode(text: str, shift=3) -> str

def get_md5_str(s: str) -> str

def rot13(s: str) -> str
"""

import hashlib
import string

from chepy import Chepy


def caesar_encode(text: str, shift=3) -> str:
    """
    凯撒编码

    编码和解码都用这个函数，只需要保证偏移相同

    shift: 偏移量，默认为 3
    """
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(shifted_alphabet, alphabet)
    return text.translate(table)


def get_md5_str(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()

def rot13(s: str) -> str:
    """
    ROT13 编码

    编码和解码都用这个函数
    """
    return Chepy(s).rot_13().out.decode()