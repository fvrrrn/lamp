from collections.abc import Iterator
from math import gcd

# TODO: use DynHashTable example when moving NativeDictionary to demonstration
# that way __setitem__ is more likely to record element


# Euler's totient function always returns at least 1 int if n > 1
def coprime(n: int) -> int:
    for i in range(1, n):
        if gcd(i, n) == 1:
            return i
    raise AssertionError(f"No coprime step found for size={n}")


class NativeDictionary[T]:
    def __init__(self, sz):
        self.size = sz
        self.step = coprime(sz) if self.size > 1 else 1
        self.slots: list[str | None] = [None] * self.size
        self.values: list[T | None] = [None] * self.size
        self.__modulo = 1234567891  # closest prime to 2**32 which is max int
        self.__base = 67  # 67 is the closest prime to 62 which is 23 lowercase latin letters + 23 uppercase + 10 digits  # noqa: E501
        self.__size = 0

    def hash_fun(self, key: str) -> int:
        hash_value = 0
        power = 1
        for c in reversed(key):
            hash_value = (hash_value + ord(c) * power) % self.__modulo
            power = (power * self.__base) % self.__modulo
        return hash_value % self.size

    def __slots_iter(self, key: str) -> Iterator[int]:
        start = self.hash_fun(key)
        for i in range(self.size // gcd(self.size, self.step)):
            yield (start + i * self.step) % self.size

    def seek_slot(self, key: str) -> int | None:
        for index in self.__slots_iter(key):
            if self.slots[index] is None or self.slots[index] == key:
                return index
        return None

    def is_key(self, key: str) -> bool:
        return any(self.slots[index] == key for index in self.__slots_iter(key))

    # TODO: add Maybe[int] after server tests
    def put(self, key: str, value: T):
        if (index := self.seek_slot(key)) is not None:
            self.__size += self.slots[index] != key
            # TODO: with dynamic resizing change step on each self.size change
            self.slots[index] = key
            self.values[index] = value
            return index

    def get(self, key: str) -> T | None:
        for index in self.__slots_iter(key):
            if self.slots[index] == key:
                return self.values[index]

    def __len__(self) -> int:
        return self.__size

    def __setitem__(self, key: str, value: T) -> int | None:
        return self.put(key, value)

    def __getitem__(self, key: str) -> T | None:
        return self.get(key)
