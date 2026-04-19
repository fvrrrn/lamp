import ctypes
from collections.abc import Iterator
from typing import NoReturn


class DynArray[T]:
    def __str__(self):
        return "[" + ", ".join(str(self.array[i]) for i in range(self.count)) + "]"

    # tests mail fail if constructor takes parameters so magic number default are used
    def __init__(self):
        self.count = 0
        self.capacity = 16
        self.array = self.make_array(self.capacity)

    def __len__(self):
        return self.count

    def __iter__(self) -> Iterator[T]:
        for i in range(0, self.count):
            yield self.array[i]

    def make_array(self, new_capacity):
        return (new_capacity * ctypes.py_object)()

    def __getitem__(self, i: int) -> T | NoReturn:
        if i < 0 or i >= self.count:
            raise IndexError("Index is out of bounds")
        return self.array[i]

    def resize(self, new_capacity):
        new_array = self.make_array(new_capacity)
        for i in range(self.count):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity

    def append(self, itm: T):
        if self.count == self.capacity:
            self.resize(2 * self.capacity)
        self.array[self.count] = itm
        self.count += 1

    def insert(self, i: int, itm: T):
        if i < 0 or i > self.count:
            raise IndexError("Index is out of bounds")
        if self.count == self.capacity:
            self.resize(2 * self.capacity)
        for j in range(self.count, i, -1):
            self.array[j] = self.array[j - 1]
        self.array[i] = itm
        self.count += 1

    def delete(self, i: int):
        if i < 0 or i >= self.count:
            raise IndexError("Index is out of bounds")
        for j in range(i, self.count - 1):
            self.array[j] = self.array[j + 1]
        self.count -= 1
        if self.count < 0.5 * self.capacity:
            new_capacity = max(int(self.capacity / 1.5), 16)
            self.resize(new_capacity)
