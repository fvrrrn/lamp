import operator
from collections.abc import Callable
from functools import reduce


class BloomFilter:
    def __init__(
        self,
        f_len: int,
        bit_array: int = 0,
        *hash_fns: Callable[[str], int],
    ):
        self.f_len = f_len
        self.bit_array = bit_array
        # cannot set default parameter to * and ** types
        self.hash_fns = (
            list(hash_fns)
            if hash_fns
            else [
                lambda s: 1 << (hash1(s) % self.f_len),
                lambda s: 1 << (hash2(s) % self.f_len),
            ]
        )

    def __str__(self):
        return bin(self.bit_array)

    # TODO: remove after tests passed
    def hash1(self, str1: str) -> int:
        return sum(ord(c) * (17**i) for i, c in enumerate(str1)) % self.f_len

    # TODO: remove after tests passed
    def hash2(self, str1: str) -> int:
        return sum(ord(c) * (223**i) for i, c in enumerate(str1)) % self.f_len

    def add(self, str1: str):
        self.bit_array |= reduce(operator.or_, (f(str1) for f in self.hash_fns))

    def is_value(self, str1: str) -> bool:
        mask = reduce(operator.or_, (f(str1) for f in self.hash_fns))
        return mask == (self.bit_array & mask)


def hash1(str1: str) -> int:
    hash_value = 0
    power = 1
    for c in str1:
        hash_value += ord(c) * power
        power *= 17
    return hash_value


def hash2(str1: str) -> int:
    hash_value = 0
    power = 1
    for c in str1:
        hash_value += ord(c) * power
        power *= 223
    return hash_value
