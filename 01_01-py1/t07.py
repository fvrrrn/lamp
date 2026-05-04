from collections.abc import Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import SupportsDunderLT


class _Sentinel[T]:
    prev: "_Sentinel[T] | Node[T]"
    next: "_Sentinel[T] | Node[T]"


class Node[T]:
    def __init__(self, value: T) -> None:
        self.value = value

    prev: "Node[T] | _Sentinel[T]"
    next: "Node[T] | _Sentinel[T]"
    value: T


class OrderedList[T: SupportsDunderLT]:
    def __init__(self, asc, *values: T) -> None:
        self.__head = _Sentinel()
        self.__tail = self.__head
        self.__head.next = self.__tail
        self.__tail.prev = self.__head
        self.__head.prev = self.__tail
        self.__tail.next = self.__head
        self.size = 0
        self.__ascending = asc
        for v in values:
            self.add(v)

    @property
    def is_asc(self) -> bool:
        return self.__ascending

    # just to be safe there won't be type errors because of Literal[-1, 0, 1]
    def compare(self, v1: T, v2: T) -> int:
        if v1 < v2:
            return -1
        if v1 == v2:
            return 0
        return 1

    def add(self, value: T) -> None:
        node = self.__head.next
        while True:
            match node:
                case _Sentinel():
                    break
                case Node():
                    match self.__ascending, self.compare(node.value, value):
                        case True, (0 | 1):
                            break
                        case False, (0 | -1):
                            break
                    node = node.next

        new_node = Node(value)
        new_node.prev = node.prev
        new_node.next = node
        node.prev.next = new_node
        node.prev = new_node
        self.size += 1

    def unsafe_append(self, value: T) -> Node[T]:
        node = Node(value)
        node.prev = self.__tail.prev
        node.next = self.__tail
        self.__tail.prev.next = node
        self.__tail.prev = node
        self.size += 1
        return node

    def find(self, val: T) -> Node[T] | None:
        node = self.__head.next
        while True:
            match node:
                case _Sentinel():
                    return None
                case Node():
                    cmp = self.compare(node.value, val)
                    if cmp == 0:
                        return node
                    # early termination: passed the insertion point
                    if (self.__ascending and cmp == 1) or (not self.__ascending and cmp == -1):
                        return None
                    node = node.next

    def delete(self, val: T):
        node = self.find(val)
        if node is not None:
            node.prev.next = node.next
            node.next.prev = node.prev
            self.size -= 1

    def clean(self, asc):
        self.__ascending = asc
        self.__head.next = self.__tail
        self.__tail.prev = self.__head
        self.__head.prev = self.__tail
        self.__tail.next = self.__head
        self.size = 0

    def len(self):
        return self.size

    def get_all(self):
        r = []
        node = self.__head.next
        while not isinstance(node, _Sentinel):
            r.append(node)
            node = node.next
        return r

    def __iter__(self) -> Iterator[T]:
        node = self.__head.next
        while True:
            match node:
                case _Sentinel():
                    break
                case Node():
                    yield node.value
                    node = node.next

    def __reversed__(self) -> Iterator[T]:
        node = self.__tail.prev
        while True:
            match node:
                case _Sentinel():
                    break
                case Node():
                    yield node.value
                    node = node.prev

    def __len__(self):
        return self.size

    def __str__(self):
        return " -> ".join(str(value) for value in self)

    # greedy-iest way to do that
    # but linked list optimizations barely improve speed
    # it is best to have array-based implementation with binary search from the next task
    def __contains__(self, sublist: "OrderedList[T]") -> bool:
        if len(sublist) == 0:
            return True

        selflist = list(self)
        for i in range(len(selflist) - len(sublist) + 1):
            if selflist[i : i + len(sublist)] == list(sublist):
                return True

        return False


class OrderedStringList(OrderedList[str]):
    def __init__(self, asc):
        super().__init__(asc)

    def compare(self, v1, v2):
        stripped_v1 = v1.strip()
        stripped_v2 = v2.strip()

        if stripped_v1 < stripped_v2:
            return -1
        if stripped_v1 == stripped_v2:
            return 0
        return 1
