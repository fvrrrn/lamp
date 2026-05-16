from collections.abc import Callable
from itertools import product

from t11 import BloomFilter, hash1, hash2


# TASK: 1.11.2*
# TITLE: Bloom filter merge
# TIME COMPLEXITY: O(1)
# SPACE COMPLEXITY: O(1) does not depend on hash_fns size
# REFLECTION:
#   - Probability of false-positivity does not change on filter merge
#     because it only depends on `m` and `n` where m is f_len and n is len(str)
#   - `str` string-only hash function parameter can be expanded to generic `Hashable`
#   - *hash_fns can be changed to just List[hash_fns] and have default parameter
#   - .bit_length() how many bits total
#   - .bit_count() how many bits=1 total
#   - Python adds bits on demand so binary representation of `int i = 0;` is `0` and not `0...0`
#   - compare self.f_len and other.f_len
class AddableBloomFilter(BloomFilter):
    def __add__(self, other: "AddableBloomFilter"):
        return AddableBloomFilter(
            self.f_len,
            self.bit_array | other.bit_array,
            *(self.hash_fns + other.hash_fns),
        )


# TASK: 1.11.3*
# TITLE: Bloom filter with removable elements
# TIME COMPLEXITY: O(1) hash_fns and bit_array iterations do not depend on elements amount
# SPACE COMPLEXITY: O(1) though array is used its size does not depend on elements amount
# REFLECTION:
#   - hash function should just only hash (duh), there shouldn't be modulo or bit-shift and whatnot
#   - there can be interger overflow in `add`
class RemovableBloomFilter(BloomFilter):
    def __init__(
        self,
        f_len: int,
        *hash_fns: Callable[[str], int],
    ):
        self.f_len = f_len
        self.bit_array = [0] * self.f_len
        # cannot set default parameter to * and ** types
        self.hash_fns = (
            list(hash_fns)
            if hash_fns
            else [
                lambda s: hash1(s) % self.f_len,
                lambda s: hash2(s) % self.f_len,
            ]
        )

    def __str__(self) -> str:
        return str(self.bit_array)

    def add(self, str1: str):
        for f in self.hash_fns:
            self.bit_array[f(str1)] += 1

    def is_value(self, str1: str) -> bool:
        mask = [0] * self.f_len
        for f in self.hash_fns:
            mask[f(str1)] += 1
        return all(not (e1 > 0 and e1 > e2) for e1, e2 in zip(mask, self.bit_array, strict=False))

    def remove(self, str1: str):
        for f in self.hash_fns:
            self.bit_array[f(str1)] = max(0, self.bit_array[f(str1)] - 1)


# TASK: 1.11.4*
# TITLE: Bloom filter elements reconstruction
# TIME COMPLEXITY: O(p ^ n) where is power of alphabet
# SPACE COMPLEXITY: O(p ^ n) to store all the elements
# REFLECTION:
#   - 1. Let k = len(bloom_filter.hash_fns), m = bloom_filter.bit_array.bit_length(), k = 0,6931 * m / n
#     Then n = m * 0.6931 / k
#     2. For all possible ordered n repeatable combinations of values of str (0-9a-zA-Z, emoji etc.)
#     check if given string of such combination is within bloom filter
#   - Knowing beforehand what symbols we are after could significantly improve performance (for instance phone numbers)
#   - Can be parallelized or ran with GPU since we are doing binary operations
#   - TODO: 0.6931 is ln 2, check why
# CODE:
def reconstruct(bloom_filter: BloomFilter) -> list[str]:
    result: list[str] = []
    k = len(bloom_filter.hash_fns)
    m = bloom_filter.bit_array.bit_length()
    n = min(1, int(round(m * 0.6931) / k))
    for chars in product("0123456789", repeat=n):
        candidate = "".join(chars)
        if bloom_filter.is_value(candidate):
            result += candidate
    return result
