from collections.abc import Iterator


# making _Sentinel generic allows getting correct type for Node
class _Sentinel[T]:
    prev: "_Sentinel[T] | Node[T]"
    next: "_Sentinel[T] | Node[T]"


class Node[T]:
    def __init__(self, value: T) -> None:
        self.value = value

    prev: "Node[T] | _Sentinel[T]"
    next: "Node[T] | _Sentinel[T]"
    value: T


class Queue[T]:
    def __init__(self, *values: T) -> None:
        self._head = _Sentinel[T]()
        self._tail = _Sentinel[T]()
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0
        for value in values:
            self.enqueue(value)

    def size(self):
        return self._size

    def enqueue(self, value: T) -> None:
        """Add an element to the end of the queue
        O(1) time complexity and O(1) space complexity.

        Args:
            value (T): The value to be added to the queue.

        Returns:
            Node[T]: The node containing the enqueued value.
        """
        node = Node(value)
        node.prev = self._tail.prev
        node.next = self._tail
        self._tail.prev.next = node
        self._tail.prev = node
        self._size += 1
        # return node

    def dequeue(self) -> T | None:
        """Remove and return the first element from the queue
        O(1) time complexity and O(1) space complexity.

        Returns:
            T | None: The value of the dequeued node, or None if the queue is empty.
        """
        match self._head.next:
            case _Sentinel():
                return None
            case Node():
                value = self._head.next.value
                self._head.next = self._head.next.next
                self._head.next.prev = self._head
                self._size -= 1
                return value

    def __iter__(self) -> Iterator[T]:
        node = self._head.next
        # prevent infinite loop if cycles are present
        for _ in range(self._size):
            match node:
                case _Sentinel():
                    break
                case Node():
                    yield node.value
                    node = node.next

    def __reversed__(self) -> Iterator[T]:
        node = self._tail.prev
        # prevent infinite loop if cycles are present
        for _ in range(self._size):
            match node:
                case _Sentinel():
                    break
                case Node():
                    yield node.value
                    node = node.prev

    def __getitem__(self, index: int) -> T:
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        for i, value in enumerate(self):
            if i == index:
                return value
        # unreachable because of check above
        raise IndexError("Index out of range")

    def __setitem__(self, index: int, value: T) -> None:
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        node = self._head.next
        for _ in range(index):
            node = node.next
        match node:
            case _Sentinel():
                raise IndexError("Index out of range")
            case Node():
                node.value = value

    def __len__(self):
        return self._size

    def __str__(self):
        return " -> ".join(str(value) for value in self)
