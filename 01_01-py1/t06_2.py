# ruff: noqa: N802
import bisect
from collections.abc import Iterator
from typing import Protocol, TypeVar

from t03 import DynArray
from t06 import Deque


# from _typeshed import SupportsDunderLT -> ModuleNotFoundError: No module named '_typeshed'
class SupportsBool(Protocol):
    def __bool__(self) -> bool: ...


_T_contra = TypeVar("_T_contra", contravariant=True)


class SupportsDunderLT(Protocol[_T_contra]):
    def __lt__(self, other: _T_contra, /) -> SupportsBool: ...


# TASK: 1.6.1
# TITLE: Complexity analysis for Deque backed by a Python list/array
# REFLECTION:
#     If the Python list's index-0 end is the head (front), then:
#     - addFront / removeFront use list.insert(0) / list.pop(0): O(n) because
#       every existing element must be shifted one position.
#     - addTail / removeTail use list.append() / list.pop(): O(1) amortized
#       because no shifting is needed.
#     Choosing the list's last index as the front inverts the picture.
#     The doubly-linked-list implementation in t06.py avoids this asymmetry:
#     all four operations are O(1) regardless of which end is called "front".


# TASK: 1.6.2
# TITLE: Tests for all four methods
# ./t06_3.py


# TASK: 1.6.3
# TITLE: Check whether a string is a palindrome using a deque
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(n)
# REFLECTION:
#     Does not beat two-pointer O(1) space O(n) time solution though
def is_string_palindrome(text: str) -> bool:
    dq: Deque[str] = Deque()
    for char in text:
        dq.addTail(char)
    while dq.size() > 1:
        if dq.removeFront() != dq.removeTail():
            return False
    return True


# 7.4.* Minimum element in O(1)
# TASK: 1.6.4
# TITLE: Deque with O(1) minimum via two parallel min stacks
# TIME COMPLEXITY:
#     addFront O(log n), addTail O(log n),
#     removeFront O(1) amortized, removeTail O(1) amortized,
#     _min O(1)
# SPACE COMPLEXITY: O(n)
# REFLECTION:
#     A single sorted list tracks all deque elements. bisect.insort keeps it
#     sorted on every add (O(n) due to the shift, O(log n) for the search).
#     Removal calls list.remove which is O(n). The payoff: _min is always
#     _sorted[0], an O(1) read with no extra stack bookkeeping needed.
class MinDeque[T: SupportsDunderLT](Deque[T]):
    def __init__(self):
        super().__init__()
        self._sorted: list[T] = []

    def addFront(self, item: T) -> None:
        super().addFront(item)
        bisect.insort(self._sorted, item)

    def addTail(self, item: T) -> None:
        super().addTail(item)
        bisect.insort(self._sorted, item)

    def removeFront(self) -> T | None:
        if value := super().removeFront():
            self._sorted.remove(value)
            return value

    def removeTail(self) -> T | None:
        if value := super().removeTail():
            self._sorted.remove(value)
            return value

    @property
    def _min(self) -> T | None:
        return self._sorted[0] if self._sorted else None


# 7.5.* Deque backed by a dynamic array
# TASK: 1.6.5
# TITLE: Deque backed by a dynamic array with O(1) amortized add/remove
# TIME COMPLEXITY:
#     addFront O(n) worst case / O(1) amortized if using offset trick,
#     addTail O(1) amortized, removeFront O(n), removeTail O(1) amortized
# SPACE COMPLEXITY: O(n)
# REFLECTION:
#     DynArray (from t03) is a standard dynamic array (like Python's list).
#     addTail maps to append -- O(1) amortized because doubling ensures each
#     element is copied O(1) times on average.
#     addFront maps to insert(0) which shifts all n existing elements: O(n).
#     A true O(1) amortized addFront requires a "ring buffer with a front
#     pointer" (like Python's collections.deque): maintain head and tail
#     indices and wrap around the array. Since DynArray doesn't expose that
#     interface, the O(n) shift is accepted here.
class ArrayDeque[T]:
    def __init__(self):
        self.array = DynArray[T]()

    def addFront(self, item: T):
        self.array.insert(0, item)

    def addTail(self, item: T):
        self.array.append(item)

    def removeFront(self) -> T | None:
        try:
            return self.array.delete(0)
        except IndexError:
            return None

    def removeTail(self) -> T | None:
        try:
            return self.array.delete(len(self.array) - 1)
        except IndexError:
            return None

    def size(self) -> int:
        return len(self.array)

    def __iter__(self) -> Iterator[T]:
        return iter(self.array)

    def __str__(self) -> str:
        return str(self.array)


# 7.6.* Bracket balance check using a stack
# TASK: 1.6.6
# TITLE: Check balanced brackets in O(n) using a stack
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(n)
# REFLECTION:
#     Same as stack I guess
def is_balanced(brackets: str, mapped_brackets=None) -> bool:

    if mapped_brackets is None:
        mapped_brackets = {"(": ")", "{": "}", "[": "]"}

    stack: Deque[str] = Deque()

    for bracket in brackets:
        if bracket in mapped_brackets:
            stack.addTail(bracket)
            continue
        last_open = stack.removeTail()
        if last_open is None or mapped_brackets.get(last_open) != bracket:
            return False

    return len(stack) == 0
