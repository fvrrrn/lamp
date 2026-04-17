from collections.abc import Iterator

from t02 import LinkedList2, Node, SupportsDunderLT


class ReversibleLinkedList2[T: SupportsDunderLT](LinkedList2[T]):
    # TASK: 1.2.10
    # TITLE: Iterate doubly linked list in reverse order
    # TIME COMPLEXITY: O(n)
    # SPACE COMPLEXITY: O(1)
    # REFLECTION: -
    def __reversed__(self) -> Iterator[T]:
        node = self.tail
        while node is not None:
            yield node.value
            node = node.prev


class LoopLinkedList2[T: SupportsDunderLT](LinkedList2[T]):
    # TASK: 1.2.11
    # TITLE: Detect whether the list contains a cycle
    # TIME COMPLEXITY: O(n)
    # SPACE COMPLEXITY: O(1)
    # REFLECTION:
    #     Uses the stored size as a step budget: a loop-free list must reach
    #     None in exactly size steps from head. An alternative is Floyd's
    #     two-pointer algorithm, which also runs O(n)/O(1) but does not rely
    #     on a trusted size field -- useful if the counter could be corrupted.
    def has_loop(self) -> bool:
        node = self.head
        for _ in range(len(self)):
            if node is None:
                return False
            node = node.next
        return node is not None


class SortableLinkedList2[T: SupportsDunderLT](LinkedList2[T]):
    # TASK: 1.2.12
    # TITLE: Yield node values to enable sorted() on the list
    # TIME COMPLEXITY: O(n * log n)
    # SPACE COMPLEXITY: O(n)
    # REFLECTION:
    #     Cannot overload __sorted__ because it is directly linked to C,
    # sorted(list(LinkedList2(3,1,2))) -> [1,2,3]

    # TASK: 1.2.12
    # TITLE: Sort linked list in-place via bubble sort
    # TIME COMPLEXITY: O(n^2)
    # SPACE COMPLEXITY: O(1)
    # REFLECTION:
    #     Swaps values rather than relinking nodes, avoiding pointer bookkeeping.
    #     end_position shrinks the unsorted window by one node each outer pass.
    def mutable_sort(self) -> "SortableLinkedList2[T]":
        if self.head is None or self.tail is None:
            return self

        end_position = self.tail
        while end_position is not self.head:
            position = self.head
            while position is not end_position:
                next_node = position.next
                if next_node is None:
                    break
                if position.value > next_node.value:
                    position.value, next_node.value = next_node.value, position.value
                position = next_node
            prev_node = end_position.prev
            if prev_node is None:
                break
            end_position = prev_node
        return self


class MergeableLinkedList2[T: SupportsDunderLT](LinkedList2[T]):
    # TASK: 1.2.13
    # TITLE: Merge two sorted linked lists into a third sorted list
    # TIME COMPLEXITY: O(n^2) -- because of mutable_sort; merge step is O(n)
    # SPACE COMPLEXITY: O(n) -- new merged list of n nodes
    # REFLECTION:
    #     Merging and then sorting would improve complexity to O(n log n).
    @staticmethod
    def merge[U: SupportsDunderLT](
        l1: SortableLinkedList2[U],
        l2: SortableLinkedList2[U],
    ) -> LinkedList2[U]:
        sorted_l1 = l1.mutable_sort()
        sorted_l2 = l2.mutable_sort()
        merged: LinkedList2[U] = LinkedList2()
        current1 = sorted_l1.head
        current2 = sorted_l2.head
        while True:
            match current1, current2:
                case None, None:
                    return merged
                case _, None:
                    merged.add_in_tail(Node(current1.value))
                    current1 = current1.next
                case None, _:
                    merged.add_in_tail(Node(current2.value))
                    current2 = current2.next
                case _, _:
                    if not (current1.value < current2.value):
                        merged.add_in_tail(Node(current2.value))
                        current2 = current2.next
                    else:
                        merged.add_in_tail(Node(current1.value))
                        current1 = current1.next


# 1.2.14.* Implement a linked list using dummy sentinel nodes (Stanford CS106B).
class Node2[T: SupportsDunderLT]:
    def __init__(self, v: T) -> None:
        self.value: T = v
        self.next: Node2[T] | Dummy
        self.prev: Node2[T] | Dummy

    def __repr__(self) -> str:
        return f"Node2({self.value})"


class Dummy(Node2):
    def __init__(self) -> None:
        super().__init__(None)

    def __repr__(self) -> str:
        return "Dummy()"

    def __str__(self) -> str:
        return "Dummy"


class DummyLinkedList[T: SupportsDunderLT]:
    # TASK: 1.2.14
    # TITLE: Doubly linked list with dummy sentinel nodes
    # TIME COMPLEXITY: append/prepend/delete O(1); find/iter O(n)
    # SPACE COMPLEXITY: O(n) nodes + 2 permanent sentinels
    # REFLECTION:
    #     If for some reason Node's value is None we cannot distinguish if
    #     there are no elements or element's value is "zero"
    #     I will add Maybe or Either monads next time
    def __init__(self, *values: T) -> None:
        self._head = Dummy()
        self._tail = Dummy()
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0
        for value in values:
            self.append(value)

    @property
    def head(self) -> T | None:
        match self._head.next:
            case Dummy():
                return None
            case Node2():
                return self._head.next.value

    def __iter__(self) -> Iterator[Node2[T]]:
        node = self._head.next
        # prevent infinite loop if cycles are present
        for _ in range(self._size):
            match node:
                case Dummy():
                    break
                case Node2():
                    yield node
                    node = node.next

    def __len__(self):
        return self._size

    def __str__(self):
        return " -> ".join(str(node.value) for node in self)

    def __reversed__(self):
        node = self._tail.prev
        # prevent infinite loop if cycles are present
        for _ in range(self._size):
            match node:
                case Dummy():
                    break
                case Node2():
                    yield node
                    node = node.prev

    def __getitem__(self, index: int) -> Node2[T] | None:
        if not (0 <= index < self._size):
            return None
        node = self._head
        for _ in range(index):
            if node is not None:
                node = node.next
        if node is None:
            return None
        return node

    def prepend(self, value: T) -> Node2[T]:
        node = Node2(value)
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node
        self._size += 1
        return node

    def append(self, value: T) -> Node2[T]:
        node = Node2(value)
        node.prev = self._tail.prev
        node.next = self._tail
        self._tail.prev.next = node
        self._tail.prev = node
        self._size += 1
        return node

    def find(self, val: T) -> Node2[T] | None:
        return next((node for node in self if node.value == val), None)

    def find_all(self, val: T) -> list[Node2[T]]:
        return [node for node in self if node.value == val]

    def delete(self, val: T, all: bool = False) -> None:
        for node in self.find_all(val):
            node.prev.next = node.next
            node.next.prev = node.prev
            self._size -= 1
            if all is False:
                return

    def clean(self) -> None:
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0
