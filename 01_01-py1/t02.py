from collections.abc import Iterator
from typing import Protocol, TypeVar


# from _typeshed import SupportsDunderLT -> ModuleNotFoundError: No module named '_typeshed'
class SupportsBool(Protocol):
    def __bool__(self) -> bool: ...


_T_contra = TypeVar("_T_contra", contravariant=True)


class SupportsDunderLT(Protocol[_T_contra]):
    def __lt__(self, other: _T_contra, /) -> SupportsBool: ...


class Node[T: SupportsDunderLT]:
    def __init__(self, v: T) -> None:
        self.value: T = v
        self.next: Node[T] | None = None
        self.prev: Node[T] | None = None


class LinkedList2[T: SupportsDunderLT]:
    def __init__(self, *values: T) -> None:
        self.head: Node[T] | None = None
        self.tail: Node[T] | None = None
        self.size = 0
        for v in values:
            self.add_in_tail(Node(v))

    def __iter__(self) -> Iterator[T]:
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def __len__(self):
        return self.size

    def __str__(self):
        node = self.head
        s = ""
        while node is not None:
            s += f"{node.value} -> "
            node = node.next
        return s

    def add_in_head(self, item: Node[T]) -> None:
        match self.head, self.tail:
            case None, None:
                self.head = item
                self.tail = item
                self.size += 1
            case _, None:
                pass
            case None, _:
                pass
            case _, _:
                item.next = self.head
                self.head.prev = item
                self.head = item
                self.size += 1

    def add_in_tail(self, item: Node[T]) -> None:
        match self.head, self.tail:
            case None, None:
                self.head = item
                self.tail = item
                self.size += 1
            case _, None:
                pass
            case None, _:
                pass
            case _, _:
                self.tail.next = item
                item.prev = self.tail
                self.tail = item
                self.size += 1

    def print_all_nodes(self) -> None:
        node = self.head
        while node is not None:
            print(node.value)  # noqa: T201
            node = node.next

    def find(self, val: T) -> Node[T] | None:
        node = self.head
        while node is not None:
            if node.value == val:
                return node
            node = node.next
        return None

    def find_all(self, val: T) -> list[Node[T]]:
        result = []
        node = self.head
        while node is not None:
            if node.value == val:
                result.append(node)
            node = node.next
        return result

    def delete(self, val: T, all: bool = False) -> None:
        for node in self.find_all(val):
            if self.head is None or self.tail is None:
                break
            match node == self.head, node == self.tail:
                case True, True:
                    self.head = None
                    self.tail = None
                case True, False:
                    if head_next := self.head.next:
                        head_next.prev = None
                        self.head = head_next
                case False, True:
                    if tail_prev := self.tail.prev:
                        tail_prev.next = None
                        self.tail = tail_prev
                case False, False:
                    if (node_prev := node.prev) and (node_next := node.next):
                        node_prev.next = node_next
                        node_next.prev = node_prev
            self.size -= 1
            if all is False:
                return

    def clean(self) -> None:
        self.head = None
        self.tail = None
        self.size = 0

    def len(self) -> int:
        return self.size

    def insert(self, afterNode: Node[T] | None, newNode: Node[T]) -> None:  # noqa: N803
        match self.head, self.tail, afterNode:
            case None, None, None:
                self.add_in_tail(newNode)
            case None, _, _:
                pass
            case _, None, _:
                pass
            case _, _, None:
                self.tail.next = newNode
                newNode.prev = self.tail
                self.tail = newNode
                self.size += 1
            case _, _, _:
                if afterNode.next is None:
                    afterNode.next = newNode
                    newNode.prev = afterNode
                    self.size += 1
                    self.tail = newNode
                else:
                    afterNode.next.prev = newNode
                    newNode.next = afterNode.next
                    afterNode.next = newNode
                    newNode.prev = afterNode
                    self.size += 1
