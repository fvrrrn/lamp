from collections.abc import Sequence

from t03 import DynArray


class BankedResizePolicy:
    def can_resize(self, bank: int, count: int) -> bool:
        return bank >= count

    def deduct(self, bank: int, count: int) -> int:
        return bank - count


# TASK: 1.3.5
# TITLE: Dynamic array with amortized O(1) append proven by the bank method
# TIME COMPLEXITY: append O(1) amortized, resize O(n), insert O(n)
# SPACE COMPLEXITY: O(n)
# REFLECTION:
#     Because tests may fail if constructor takes parameters here again we use magic `2`
#     Whereas addition_factor is actually a capacity multiplier.
#     Here we do a proof that is append is actually O(1) because bank's grow is linear (+=)
#     Let count be capacity/2, tokens before resizing accumulated is 2 * capacity/2
#     Therefore, bank = count, and since bank is linear so is count, q.e.d.
#     BankedResizePolicy separates the bank accounting from resize so that resize
#     not violating Liskov's Substitution Principle,
#     keeps the same preconditions as the parent (no RuntimeError added).
class DynArray2[T](DynArray[T]):
    def __init__(self) -> None:
        super().__init__()
        self.bank = 0
        self.addition_factor = 2  # = self.resize_multiplier
        self._resize_policy = BankedResizePolicy()

    def resize(self, new_capacity: int) -> None:
        self.bank = self._resize_policy.deduct(self.bank, self.count)
        super().resize(new_capacity)

    def append(self, itm: T) -> None:
        self.bank += self.addition_factor
        super().append(itm)

    def insert(self, i: int, itm: T) -> None:
        self.bank += self.addition_factor
        super().insert(i, itm)


# TASK: 1.3.6
# TITLE: Multi-dimensional dynamic array with per-axis DynArray nesting
# TIME COMPLEXITY: __init__ O(prod(level)), __getitem__ O(d), __setitem__ O(d) + growth
# SPACE COMPLEXITY: O(prod(level)) initial; grows per __setitem__ calls
# REFLECTION:
#     Can overload __getitem__ so slices can be passed making it look like numpy array
class MultiDynArray:
    def __init__(self, level: list[int]) -> None:
        if not level:
            raise ValueError("level must have at least one dimension")
        self.dim = len(level)
        self.level = list(level)
        self.array = self.make_array(level, 0)

    def make_array(self, level: list[int], depth: int) -> DynArray:
        arr = DynArray()
        size = level[0]
        if len(level) == 1:
            for _ in range(size):
                arr.append(None)
        else:
            for _ in range(size):
                arr.append(self.make_array(level[1:], depth + 1))
        return arr

    def __getitem__(self, indices: Sequence[int]) -> object:
        if len(indices) != self.dim:
            raise IndexError("Incorrect number of indices")
        current = self.array
        for i in range(len(indices)):
            idx = indices[i]
            if idx < 0 or idx >= len(current):
                raise IndexError("Index out of bounds")
            if i == self.dim - 1:
                return current[idx]
            current = current[idx]
        return None

    def __setitem__(self, indices: Sequence[int], value: object) -> None:
        if len(indices) != self.dim:
            raise IndexError("Incorrect number of indices")
        current = self.array
        for i in range(len(indices)):
            idx = indices[i]
            if idx < 0:
                raise IndexError("Index out of bounds")
            while idx >= len(current):
                if i == self.dim - 1:
                    current.append(None)
                else:
                    current.append(self.make_array(self.level[i + 1 :], i + 1))
            if i == self.dim - 1:
                current.array[idx] = value
            else:
                current = current[idx]
