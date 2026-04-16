from collections.abc import Iterator
from typing import Protocol, TypeGuard, cast


class Equalable(Protocol):
    def __eq__(self, other: object, /) -> bool: ...


class Node[T: Equalable]:
    def __init__(self, v: T) -> None:
        self.value: T = v
        self.next: Node[T] | None = None
        self.prev: Node[T] | None = None


class LinkedList[T: Equalable]:
    def __init__(self) -> None:
        self.head: Node[T] | None = None
        self.tail: Node[T] | None = None
        self.size = 0

    def __iter__(self) -> Iterator[Node[T]]:
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __len__(self):
        return self.size

    def __str__(self):
        return " -> ".join(str(node.value) for node in self)

    def __reversed__(self):
        node = self.tail
        while node is not None:
            yield node
            node = node.prev

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
        for node in self:
            print(node.value)

    def find(self, val: T) -> Node[T] | None:
        return next((node for node in self if node.value == val), None)

    def find_all(self, val: T) -> list[Node[T]]:
        return [node for node in self if node.value == val]

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
                # TypeGuard does not work with match-case
                if is_tail(afterNode):
                    afterNode.next = newNode
                    newNode.prev = cast(Node[T], afterNode)
                    self.size += 1
                    self.tail = newNode
                elif is_head(afterNode) or is_middle(afterNode):
                    afterNode.next.prev = newNode
                    newNode.next = afterNode.next
                    afterNode.next = newNode
                    newNode.prev = cast(Node[T], afterNode)
                    self.size += 1


class HasNext[T: Equalable](Protocol):
    prev: Node[T] | None
    next: Node[T]


class HasPrev[T: Equalable](Protocol):
    prev: Node[T]
    next: Node[T] | None


class HasPrevNext[T: Equalable](Protocol):
    prev: Node[T]
    next: Node[T]


def is_head[T: Equalable](node: Node[T]) -> TypeGuard[HasNext[T]]:
    return node.prev is None


def is_tail[T: Equalable](node: Node[T]) -> TypeGuard[HasPrev[T]]:
    return node.next is None


def is_middle[T: Equalable](node: Node[T]) -> TypeGuard[HasPrevNext[T]]:
    return node.prev is not None and node.next is not None
