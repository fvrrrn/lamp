from collections.abc import Iterator


class PowerSet[T]:
    def __init__(self, *elements: T) -> None:
        self.elements: dict[T, int] = {}
        for e in elements:
            self.put(e)

    def __len__(self) -> int:
        return len(self.elements)

    def size(self) -> int:
        return len(self)

    def put(self, element: T) -> None:
        self.elements[element] = 1

    def get(self, element: T) -> bool:
        return element in self

    def remove(self, element: T) -> bool:
        return self.__delitem__(element)

    def cartesian_product(self, set2: "PowerSet[T]") -> Iterator[tuple[T, T]]:
        for e1 in self:
            for e2 in set2:
                yield (e1, e2)

    def __contains__(self, element: T) -> bool:
        return bool(self.elements.get(element, 0))

    def __delitem__(self, element: T) -> bool:
        if element in self.elements:
            del self.elements[element]
            return True
        return False

    def __getitem__(self, element: T) -> int:
        return self.elements.get(element, 0)

    def __setitem__(self, element: T, value: int) -> None:
        self.elements[element] = 1 if value else 0
        # remove element if value is 0 to avoid having existing element with value 0
        if self.elements[element] == 0:
            del self.elements[element]

    def intersection(self, *sets: "PowerSet[T]") -> "PowerSet[T]":
        set3 = PowerSet()
        for e in self:
            for s in sets:
                if e in s:
                    set3.put(e)
        return set3

    def union(self, set2: "PowerSet[T]") -> "PowerSet[T]":
        set3 = PowerSet()
        for e in self:
            set3.put(e)
        for e in set2:
            set3.put(e)
        return set3

    def difference(self, set2: "PowerSet[T]") -> "PowerSet[T]":
        set3 = PowerSet()
        for e in self:
            if e not in set2:
                set3.put(e)
        return set3

    def issubset(self, set2: "PowerSet[T]") -> bool:
        return all(e in self for e in set2)

    def __iter__(self) -> Iterator[T]:
        return iter(self.elements)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PowerSet):
            return False
        if len(self) != len(other):
            return False
        return all(e2 in self and e1 in other for e1, e2 in zip(self, other, strict=False))

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def equals(self, set2: "PowerSet[T]") -> bool:
        return self == set2

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.elements})"
