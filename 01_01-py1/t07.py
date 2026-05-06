from typing import Any, Generic, Iterator, Optional, Protocol, TypeVar


class Comparable(Protocol):
    def __eq__(self, other: Any, /) -> bool: ...
    def __ne__(self, other: Any, /) -> bool: ...
    def __lt__(self, other: Any, /) -> bool: ...
    def __le__(self, other: Any, /) -> bool: ...
    def __gt__(self, other: Any, /) -> bool: ...
    def __ge__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Comparable)


class Node2(Generic[T]):
    def __init__(self, v: T) -> None:
        self.value: T = v
        self.next: Node2[T] | Dummy
        self.prev: Node2[T] | Dummy

    def __repr__(self) -> str:
        return f"Node({self.value})"


class Dummy(Node2):
    def __init__(self) -> None:
        super().__init__(None)

    def __repr__(self) -> str:
        return "Dummy()"

    def __str__(self) -> str:
        return "Dummy"


class OrderedList2(Generic[T]):
    def __init__(self, asc, *values: T) -> None:
        self.__head = Dummy()
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
                case Dummy():
                    break
                case Node2():
                    match self.__ascending, self.compare(node.value, value):
                        case True, 1:
                            break
                        case False, -1:
                            break
                    node = node.next

        new_node = Node2(value)
        new_node.prev = node.prev
        new_node.next = node
        node.prev.next = new_node
        node.prev = new_node
        self.size += 1

    def unsafe_append(self, value: T) -> Node2[T]:
        node = Node2(value)
        node.prev = self.__tail.prev
        node.next = self.__tail
        self.__tail.prev.next = node
        self.__tail.prev = node
        self.size += 1
        return node

    def find(self, val: T) -> Optional[Node2[T]]:
        node = self.__head.next

        if not isinstance(self.__head.next, Dummy):
            # node=Node(2) and val=1 return None because 2 is the smallest number
            if self.__ascending and self.compare(val, node.value) == -1:
                return None
            # node=Node(5) and val=6 return None because 6 is the largest number
            elif not self.__ascending and self.compare(val, node.value) == 1:
                return None

        while True:
            match node:
                case Dummy():
                    return None
                case Node2():
                    if node.value == val:
                        return node
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
        while not isinstance(node, Dummy):
            r.append(node)
            node = node.next
        return r

    def __iter__(self) -> Iterator[T]:
        node = self.__head.next
        while True:
            match node:
                case Dummy():
                    break
                case Node2():
                    yield node.value
                    node = node.next

    def __reversed__(self) -> Iterator[T]:
        node = self.__tail.prev
        while True:
            match node:
                case Dummy():
                    break
                case Node2():
                    yield node.value
                    node = node.prev

    def __len__(self):
        return self.size

    def __str__(self):
        return " -> ".join(str(value) for value in self)

    # greedy-iest way to do that
    # but linked list optimizations barely improve speed
    # it is best to have array-based implementation with binary search from the next task
    def __contains__(self, sublist: "OrderedList2[T]") -> bool:
        if len(sublist) == 0:
            return True

        selflist = list(self)
        for i in range(len(selflist) - len(sublist) + 1):
            if selflist[i : i + len(sublist)] == list(sublist):
                return True

        return False


class OrderedStringList2(OrderedList2[str]):
    def __init__(self, asc):
        super(OrderedStringList2, self).__init__(asc)

    def compare(self, v1, v2):
        strippedV1 = v1.strip()
        strippedV2 = v2.strip()

        if strippedV1 < strippedV2:
            return -1
        if strippedV1 == strippedV2:
            return 0
        return 1


class Node:
    def __init__(self, v):
        self.value = v
        self.prev = None
        self.next = None


class OrderedList:
    def __init__(self, asc):
        self.head = None
        self.tail = None
        self.size = 0
        self.__ascending = asc

    def compare(self, v1, v2):
        if v1 < v2:
            return -1
        if v1 == v2:
            return 0
        return 1

    def add(self, value):
        node = self.head
        direction = (0, 1) if self.__ascending else (0, -1)

        while node is not None:
            if self.compare(node.value, value) in direction:
                match node.prev is None:
                    case True:
                        self.add_in_head(Node(value))
                    case False:
                        self.insert(node.prev, Node(value))
                return

            match node is self.tail:
                case True:
                    self.insert(node, Node(value))
                    return

            node = node.next

        self.insert(None, Node(value))

    def find(self, val):
        node = self.head
        while node is not None:
            if self.compare(node.value, val) == 0:
                return node
            node = node.next
        return None

    def delete(self, val):
        node = self.find(val)
        if node is None:
            return

        match node == self.head, node == self.tail:
            case True, True:
                self.head = None
                self.tail = None
            case True, False:
                self.head = self.head.next  # type: ignore
                if self.head:
                    self.head.prev = None
            case False, True:
                self.tail = self.tail.prev  # type: ignore
                if self.tail:
                    self.tail.next = None
            case False, False:
                prev_node = node.prev
                next_node = node.next
                match prev_node, next_node:
                    case p, n if p and n:
                        p.next = n
                        n.prev = p

        self.size -= 1

    def clean(self, asc):
        self.__ascending = asc
        node = self.head
        while node is not None:
            next_node = node.next
            node.prev = None
            node.next = None
            node = next_node
        self.head = None
        self.tail = None
        self.size = 0

    def len(self):
        return self.size

    def get_all(self):
        result = []
        node = self.head
        while node is not None:
            result.append(node)
            node = node.next
        return result

    def insert(self, afterNode, newNode):
        match afterNode is None:
            case True:
                match self.head is None:
                    case True:
                        self.head = newNode
                        self.tail = newNode
                    case False:
                        newNode.prev = self.tail
                        self.tail.next = newNode  # type: ignore
                        self.tail = newNode
            case False:
                newNode.next = afterNode.next
                newNode.prev = afterNode
                afterNode.next = newNode
                if newNode.next:
                    newNode.next.prev = newNode
                if afterNode is self.tail:
                    self.tail = newNode
        self.size += 1

    def add_in_head(self, newNode):
        match self.head is None:
            case True:
                self.head = self.tail = newNode
            case False:
                newNode.next = self.head
                self.head.prev = newNode  # type: ignore
                self.head = newNode
        newNode.prev = None
        self.size += 1

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def __len__(self):
        return self.size

    def __str__(self):
        return " -> ".join(str(value) for value in self)

    def __reversed__(self):
        node = self.tail
        while node is not None:
            yield node.value
            node = node.prev


class OrderedStringList(OrderedList):
    def __init__(self, asc):
        super(OrderedStringList, self).__init__(asc)

    def compare(self, v1, v2):
        strippedV1 = v1.strip()
        strippedV2 = v2.strip()

        if strippedV1 < strippedV2:
            return -1
        if strippedV1 == strippedV2:
            return 0
        return 1
