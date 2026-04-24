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


class Stack[T]:
    def __init__(self, *values: T):
        self._head = _Sentinel[T]()
        self._tail = _Sentinel[T]()
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0
        for v in values:
            self.push(v)

    def size(self):
        return self._size

    def __str__(self):
        # can do protocol that enforces T to have __str__ method
        return ", ".join(str(value) for value in self)

    def __len__(self) -> int:
        return self._size

    def pop(self) -> T | None:
        """
        Removes and returns the top item from the stack.
        O(1) time complexity and O(1) space complexity.

        If the stack is empty, returns None.

        Returns:
            T | None: The value at the top of the stack if present,
            otherwise None if the stack is empty.
        """
        match self._head.next:
            case _Sentinel():
                return None
            case Node():
                top_node = self._head.next
                self._head.next = top_node.next
                top_node.next.prev = self._head
                self._size -= 1
                return top_node.value

    def push(self, value: T) -> None:
        """
        Adds a new value to the top of the stack.
        O(1) time complexity and O(1) space complexity.

        This method creates a new node and places it at the front of the stack.

        Args:
            value (T): The value to be added to the stack.

        Returns:
            None: This method does not return a value.
        """
        node = Node(value)
        node.next = self._head.next
        node.prev = self._head
        self._head.next.prev = node
        self._head.next = node
        self._size += 1

    def peek(self) -> T | None:
        """
        Returns the value at the top of the stack without removing it.
        O(1) time complexity and O(1) space complexity.

        If the stack is empty, returns None.

        Returns:
            T | None: The value at the top of the stack if present,
            otherwise None if the stack is empty.
        """
        match self._head.next:
            case _Sentinel():
                return None
            case Node():
                return self._head.next.value

    def __iter__(self) -> Iterator[T]:
        node = self._head.next
        while True:
            match node:
                case _Sentinel():
                    break
                case Node():
                    yield node.value
                    node = node.next

    def __reversed__(self) -> Iterator[T]:
        node = self._tail.prev
        while True:
            match node:
                case _Sentinel():
                    break
                case Node():
                    yield node.value
                    node = node.prev
