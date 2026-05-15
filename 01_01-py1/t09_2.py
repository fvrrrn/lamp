# ruff: noqa: RUF003
from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING, Literal, TypeVar

if TYPE_CHECKING:
    from _typeshed import SupportsDunderLT


from dataclasses import dataclass
from typing import TypeGuard

L = TypeVar("L")
R = TypeVar("R")


@dataclass(frozen=True)
class Left[L, R]:
    value: L


@dataclass(frozen=True)
class Right[L, R]:
    value: R


type Either[L, R] = Left[L, R] | Right[L, R]


@dataclass(frozen=True)
class Just[T]:
    value: T


@dataclass(frozen=True)
class Nothing: ...


type Maybe[T] = Just[T] | Nothing


# TODO: при каррировании функции теряется тип её параметров
# https://stackoverflow.com/questions/59859278/typing-curried-function-in-python
def either_from_throwable[L: Exception, R](
    f: Callable[..., R],  # может быть исключение
    exception: type[L] = Exception,
) -> Callable[..., Either[L, R]]:
    def inner(*args, **kwargs) -> Either[L, R]:
        try:
            return Right(f(*args, **kwargs))
        except exception as e:
            return Left(e)

    return inner


def is_left[L, R](e: Either[L, R]) -> TypeGuard[Left[L, R]]:
    return isinstance(e, Left)


def is_right[L, R](e: Either[L, R]) -> TypeGuard[Right[L, R]]:
    return isinstance(e, Right)


# TASK: 1.9.5*
# TITLE: Словарь на основе упорядоченного массива с бинарным поиском
# TIME COMPLEXITY: __setitem__ O(log n + n) - бинарный поиск + сдвиг при вставке
#                  __getitem__ O(log n)
#                  __contains__ O(log n)
# SPACE COMPLEXITY: O(n)
# REFLECTION:
#     Бинарный поиск O(log n), лучше чем линейный O(n),
#     но вставка O(n) из-за сдвига элементов при list.insert().
class OrderedDictionary[K: SupportsDunderLT, V]:
    def __init__(self):
        self.tuples: list[tuple[K, V]] = []

    def __len__(self) -> int:
        return len(self.tuples)

    def __compare(self, a: K, b: K) -> Literal[-1, 0, 1]:
        if a < b:  # type: ignore wtf
            return -1
        if a > b:  # type: ignore ">" not supported for types "K@OrderedDictionary" and "K@OrderedDictionary" [reportOperatorIssue]
            return 1
        return 0

    # TODO: add @overload __contains__(self, a: T)
    def __contains__(self, a: K) -> bool:
        match self.__binary_search(lambda t: self.__compare(t[0], a)):
            case Right():
                return True
            case Left():
                return False

    def __setitem__(self, key: K, value: V) -> Maybe[int]:
        match self.__binary_search(lambda t: self.__compare(t[0], key)):
            case Right(value=index):
                self.tuples[index] = (key, value)
                return Just(index)
            case Left(value=index):
                self.tuples.insert(index, (key, value))
                return Nothing()

    def __getitem__(self, key: K) -> Maybe[V]:
        match self.__binary_search(lambda t: self.__compare(t[0], key)):
            case Right(value=index):
                return Just(self.tuples[index][1])
            case Left():
                return Nothing()

    def __binary_search(
        self,
        predicate: Callable[[tuple[K, V]], Literal[-1, 0, 1]],
        # either element index or insertion index
    ) -> Either[int, int]:
        left, right = 0, len(self.tuples) - 1
        while left <= right:
            mid_index = (left + right) // 2
            t = self.tuples[mid_index]
            match predicate(t):
                case -1:
                    right = mid_index - 1
                case 0:
                    return Right(mid_index)
                case 1:
                    left = mid_index + 1
        return Left(left)

    def __iter__(self) -> Iterator[tuple[K, V]]:
        return iter(self.tuples)

    def __str__(self) -> str:
        return str(self.tuples)


# TASK: 1.9.6*
# TITLE: Словарь с битовыми операциями вместо modulo
# TIME COMPLEXITY: put/get/is_key O(1) среднее, O(n) при кластеризации
#                  seek_slot O(1) среднее, O(n) худшее
# SPACE COMPLEXITY: O(n)
# REFLECTION:
#     Размер таблицы всегда степень двойки, поэтому вместо hash % size
#     можно использовать hash & (size - 1), битовая маска работает
#     быстрее деления с остатком. То же самое при линейном пробировании:
#     (index + step) & (size - 1) вместо (index + step) % size.
class BitDictionary[T]:
    def __init__(self, sz=16):
        self.size = BitDictionary.__round_power_2(sz)
        # TODO: check what step optimization can be made with bits
        self.step = 1
        self.slots: list[str | None] = [None] * self.size
        self.values: list[T | None] = [None] * self.size
        self.__base = 64
        self.__size = 0

    @staticmethod
    def __round_power_2(n: int) -> int:
        # 1 -> 1, 5 -> 8, 15 -> 16, 32 -> 32
        if n <= 1:
            return 1
        return 1 << (n - 1).bit_length()

    def hash_fun(self, key: str) -> int:
        hash_value = 0
        power = 1
        for c in reversed(key):
            hash_value += ord(c) * power
            power *= self.__base
        return hash_value & (self.size - 1)

    def __slots_iter(self, key: str) -> Iterator[int]:
        # because size if power of 2
        start = self.hash_fun(key)
        for i in range(self.size):
            yield (start + i * self.step) & (self.size - 1)

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
            # TODO: also __round_power_2
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

    def __delitem__(self, key: str) -> int | None:
        for index in self.__slots_iter(key):
            if self.slots[index] == key:
                self.values[index] = None
                self.slots[index] = None
                return index
