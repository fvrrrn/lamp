# ruff: noqa: N802


class _Sentinel[T]:
    prev: "_Sentinel[T] | Node[T]"
    next: "_Sentinel[T] | Node[T]"


class Node[T]:
    def __init__(self, value: T) -> None:
        self.value = value

    prev: "Node[T] | _Sentinel[T]"
    next: "Node[T] | _Sentinel[T]"
    value: T


class Deque[T]:
    def __init__(self):
        self._head = _Sentinel[T]()
        self._tail = _Sentinel[T]()
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0

    def addFront(self, item: T) -> None:
        node = Node(item)
        node.next = self._head.next
        node.prev = self._head
        self._head.next.prev = node
        self._head.next = node
        self._size += 1

    def addTail(self, item: T) -> None:
        node = Node(item)
        node.prev = self._tail.prev
        node.next = self._tail
        self._tail.prev.next = node
        self._tail.prev = node
        self._size += 1

    def removeFront(self) -> T | None:
        match self._head.next:
            case _Sentinel():
                return None
            case Node() as node:
                self._head.next = node.next
                node.next.prev = self._head
                self._size -= 1
                return node.value

    def removeTail(self) -> T | None:
        match self._tail.prev:
            case _Sentinel():
                return None
            case Node() as node:
                self._tail.prev = node.prev
                node.prev.next = self._tail
                self._size -= 1
                return node.value

    def size(self) -> int:
        return self._size

    def __len__(self) -> int:
        return self._size

    def is_palindrome(self) -> bool:
        items = list(self)
        return items == items[::-1]

    def __iter__(self):
        node = self._head.next
        for _ in range(self._size):
            match node:
                case _Sentinel():
                    break
                case Node() as current:
                    yield current.value
                    node = current.next

    def __str__(self) -> str:
        return " -> ".join(str(item) for item in self)
