# ruff: noqa: E501
from collections import defaultdict
from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING, Literal, Protocol

if TYPE_CHECKING:
    from _typeshed import SupportsDunderLT

from t07 import OrderedList


# TASK: 1.7.8*
# TITLE: Remove all duplicates from an ordered list
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(n)
# REFLECTION:
#     Because the list is sorted, duplicates are always adjacent
def remove_duplicates[T: SupportsDunderLT](ol: OrderedList[T]) -> OrderedList[T]:
    deduped_ol = OrderedList(ol.is_asc)
    iterator = iter(ol)
    # because list is a collection of Comparables and
    # `None` not supporting <=, >= etc.
    # currentValue can be safely set to `None` because
    # there are no elements within list that are `None`
    # however if `None` can be a value of a list,
    # I should do `class NeverEqual: __eq__() -> False __nq__() -> True`
    current_value = None
    for value in iterator:
        if value != current_value:
            deduped_ol.unsafe_append(value)
            current_value = value
    return deduped_ol


# TASK: 1.7.9*
# TITLE: Merge two ordered lists into one preserving order
# TIME COMPLEXITY: O(n + m)
# SPACE COMPLEXITY: O(n + m)
# REFLECTION:
#     Both sorted so two-pointer is enough
class IteratorStrategy[T](Protocol):
    def __iter__(self) -> Iterator[T]: ...


class ConcreteIteratorStrategyAscending[T: SupportsDunderLT](IteratorStrategy[T]):
    def __init__(self, ol: OrderedList[T]):
        self.list = ol

    def __iter__(self):
        match self.list.is_asc:
            case True:
                return iter(self.list)
            case False:
                return reversed(self.list)


class ConcreteIteratorStrategyDescending[T: SupportsDunderLT](IteratorStrategy):
    def __init__(self, ol: OrderedList[T]):
        self.list = ol

    def __iter__(self):
        match self.list.is_asc:
            case True:
                return reversed(self.list)
            case False:
                return iter(self.list)


def strategy_by_order[T: SupportsDunderLT](
    asc: bool,
) -> Callable[[OrderedList[T]], IteratorStrategy[T]]:
    match asc:
        case True:
            return ConcreteIteratorStrategyAscending
        case False:
            return ConcreteIteratorStrategyDescending


# TODO: rename IteratorStrategy to MergeStrategy and put compare in it
def compare[T: SupportsDunderLT](asc: bool, v1: T, v2: T) -> bool:
    match asc:
        case True:
            return not (v2 < v1)  # v1 <= v2 using only __lt__
        case False:
            return not (v1 < v2)  # v1 >= v2 using only __lt__


# 1. pick merged list order strategy `asc` (ascending/descending)
# 2. pick accorning iterator for each list
# for OrderedList(True, 1,2,3) it is iter() if asc=True
# for OrderedList(False, 3,2,1) it is reversed() if asc=True
# and vice versa
# 3. create pointers at the start of those iterators (e.g. [from 1,2, to 3], [to 3,2,from 1]) for asc=True)
# 4. compare pointers' values by strategy (<= for asc, >= for desc)
def merge_ordered_lists[T: SupportsDunderLT](ol1: OrderedList[T], ol2: OrderedList[T], asc: bool):
    iterator_strategy = strategy_by_order(asc)
    merged = OrderedList[T](asc=asc)
    iterator1 = iter(iterator_strategy(ol1))
    pointer1 = next(iterator1, None)
    iterator2 = iter(iterator_strategy(ol2))
    pointer2 = next(iterator2, None)
    while True:
        match pointer1, pointer2:
            case None, None:
                return merged
            case _, None:
                merged.unsafe_append(pointer1)
                pointer1 = next(iterator1, None)
            case None, _:
                merged.unsafe_append(pointer2)
                pointer2 = next(iterator2, None)
            case _, _:
                if compare(asc, pointer2, pointer1):
                    merged.unsafe_append(pointer2)
                    pointer2 = next(iterator2, None)
                else:
                    merged.unsafe_append(pointer1)
                    pointer1 = next(iterator1, None)


# TASK: 1.7.10*
# TITLE: Check whether an ordered sublist is contained in the current list
# TIME COMPLEXITY: O(n * m) worst case - slide window of length m over list of length n
# SPACE COMPLEXITY: O(n) - both lists converted to Python lists for slicing
# REFLECTION:
#     The linked-list structure offers no random access, so converting to a
#     Python list first is the most pragmatic choice.A more efficient approach (KMP / Z-algorithm)
#     would give O(n + m) but adds significant complexity.
# t07.py


# TASK: 1.7.11*
# TITLE: Find the most frequently occurring value in the list
# TIME COMPLEXITY: O(n) - single pass, dict lookup and update are O(1) amortized
# SPACE COMPLEXITY: O(k) where k is the number of distinct values
# REFLECTION:
#     A frequency dict is the natural tool here. Tracking the running maximum
#     avoids a second pass over the dict, keeping both time and code complexity
#     minimal. In case of a tie the first-encountered (smallest in asc order)
#     value wins, which is a reasonable default.
def most_common[T: SupportsDunderLT](ol: OrderedList[T]) -> T | None:
    if len(ol) == 0:
        return None

    frequency_dict = defaultdict(int)
    # sorting dict by desc and picking first element is less efficient
    max_count = 0
    result: T | None = None

    for value in ol:
        frequency_dict[value] += 1
        if frequency_dict[value] > max_count:
            max_count = frequency_dict[value]
            result = value

    return result


# TODO: implement skip list
# TASK: 1.7.12*
# TITLE: Ordered list with O(log n) index-based find backed by a dynamic array
# TIME COMPLEXITY:
#     add  O(log n) binary search + O(n) shift for list.insert
#     find O(log n) binary search
#     __getitem__ O(1)
# SPACE COMPLEXITY: O(n)
# REFLECTION:
#     Linked lists give O(1) insert once the position is known but O(n) to
#     find that position. A dynamic array inverts the trade-off: O(n) insert
#     (due to shifting) but O(log n) find via binary search.
class OrderedDynArray[T: SupportsDunderLT]:
    def __init__(self, asc: bool = True):
        self.__array: list[T] = []
        self.__ascending = asc

    def _compare(self, a: T, b: T) -> Literal[-1, 0, 1]:
        if a < b:
            return -1 if self.__ascending else 1
        if a > b:
            return 1 if self.__ascending else -1
        return 0

    def add(self, item: T):
        if not self.__array:
            self.__array.append(item)
            return

        left, right = 0, len(self.__array)
        while left < right:
            mid = (left + right) // 2
            cmp = self._compare(item, self.__array[mid])
            if cmp < 0:
                right = mid
            else:
                left = mid + 1
        self.__array.insert(left, item)

    def find(self, item: T) -> int:
        left, right = 0, len(self.__array) - 1
        while left <= right:
            mid = (left + right) // 2
            cmp = self._compare(item, self.__array[mid])
            if cmp == 0:
                return mid
            elif cmp < 0:
                right = mid - 1
            else:
                left = mid + 1
        return -1

    def __getitem__(self, i):
        return self.__array[i]

    def __len__(self):
        return len(self.__array)

    def __iter__(self):
        return iter(self.__array)

    def __reversed__(self):
        return reversed(self.__array)
