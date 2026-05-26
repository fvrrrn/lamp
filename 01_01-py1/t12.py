from collections.abc import Callable, Hashable, Iterator
from dataclasses import dataclass
from math import gcd
from typing import cast


@dataclass(frozen=True)
class Just[T]:
    value: T


@dataclass(frozen=True)
class Nothing:
    pass


type Maybe[T] = Just[T] | Nothing


# TASK: 1.12.1 Native cache
# TITLE: NativeCache with Least-Frequently-Used replacement
# TIME COMPLEXITY:
#   - __getitem__:
#       O(n) if full (finds min)
#       o(1) if load factor (s.length/s.capacity) is below certain value (which I don't know)
#       Theta(1/(1-s.length/s.capacity) if hash function creates uniform distribution
#       Omega(1) if no collision
# SPACE COMPLEXITY:
#   - O(n) where n = sz, includes slots, values, hits
# REFLECTION:
#   - with big hits it should be ordered array (or tree)
#   - with small hits as is
# CODE:
class NativeCache[K: Hashable, V]:
    def __init__(self, sz, getter: Callable[[K], V], hasher: Callable[[K], int]):
        self.size = sz
        self.dict = NativeDictionary[K, V](sz, hasher)
        self.hits: list[int] = [0] * sz
        self.getter = getter

    def __getitem__(self, key: K) -> Maybe[V]:
        maybe_index = self.dict.__contains__(key)
        match maybe_index:
            case Just(index):
                self.hits[index] += 1
                return Just(self.dict.values[index])  # type: ignore
            case _:
                # assuming getter always returns value by key
                value = self.getter(key)
                match self.dict.put(key, value):
                    case Nothing():
                        index_min = min(range(len(self.hits)), key=self.hits.__getitem__)
                        self.dict.slots[index_min] = key
                        self.dict.values[index_min] = value
                        return Just(value)
                    case _:
                        return Just(value)


# Euler's totient function always returns at least 1 int if n > 1
def coprime(n: int) -> int:
    for i in range(1, n):
        if gcd(i, n) == 1:
            return i
    raise AssertionError(f"No coprime step found for size={n}")


def polynomial_hash(s: str, base=67, mod=1234567891) -> int:
    h = 0
    for c in s:
        h = (h * base + ord(c)) % mod
    return h


class NativeDictionary[K: Hashable, V]:
    def __init__(self, sz, hasher: Callable[[K], int]):
        self.size = sz
        self.step = coprime(sz) if self.size > 1 else 1
        self.slots: list[K | None] = [None] * self.size
        self.values: list[V | None] = [None] * self.size
        self.__size = 0
        self.hasher = hasher

    def __slots_iter(self, key: K) -> Iterator[int]:
        start = self.hasher(key) % self.size
        for i in range(self.size // gcd(self.size, self.step)):
            yield (start + i * self.step) % self.size

    def seek_slot(self, key: K) -> Maybe[int]:
        for index in self.__slots_iter(key):
            if self.slots[index] is None or self.slots[index] == key:
                return Just(index)
        return Nothing()

    def put(self, key: K, value: V) -> Maybe[int]:
        match self.seek_slot(key):
            case Just(index):
                self.__size += self.slots[index] != key
                # TODO: with dynamic resizing change step on each self.size change
                self.slots[index] = key
                self.values[index] = value
                return Just(index)
            case _:
                return Nothing()

    def __contains__(self, key: K) -> Maybe[int]:
        for index in self.__slots_iter(key):
            if self.slots[index] == key:
                return Just(index)
        return Nothing()

    def get(self, key: K) -> Maybe[V]:
        match self.__contains__(key):
            case Just(value_index):
                return Just(cast(V, self.values[value_index]))
            case _:
                return Nothing()

    def __len__(self) -> int:
        return self.__size

    def __setitem__(self, key: K, value: V) -> Maybe[int]:
        return self.put(key, value)

    def __getitem__(self, key: K) -> Maybe[V]:
        return self.get(key)
