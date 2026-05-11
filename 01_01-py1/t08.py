class HashTable:
    def __init__(self, sz, stp):
        # - self.size = 17 → "table has 17 slots"
        # - self._size = 5 → "5 of those slots are
        #  filled"
        # - len(ht) returns _size
        # - load factor = _size / size
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size
        # NOTE: closest prime to 2**32 which is max int
        self.__modulo = 1234567891
        # NOTE: 67 is the closest highest prime to 62 which is 23 lowercase latin letters + 23 uppercase + 10 digits
        self.__base = 67
        self._size = 0

    # polynomial rolling hash function
    def hash_fun(self, value: str) -> int:
        hash_value = 0
        power = 1
        # NOTE: "abcd1234" -> "4321dcba" -> 4*67**0 + 3*67**1 + ...
        for c in reversed(value):
            # NOTE: using modulo at each computation to prevent overflow
            hash_value = (hash_value + ord(c) * power) % self.__modulo
            # NOTE: computing power on each tick is inneficient, multiply power by p one by one
            power = (power * self.__base) % self.__modulo
        return hash_value

    def seek_slot(self, value: str) -> int | None:
        index = self.hash_fun(value) % self.size
        # NOTE: also try `self.size / gcd(self.size, self.step)`
        for _ in range(self.size // self.step + 1):
            if self.slots[index] is None or self.slots[index] == value:
                return index
            index = (index + self.step) % self.size
        return None

    def put(self, value: str) -> int | None:
        match self.seek_slot(value):
            case None:
                return None
            case index:
                # increase only if element not in table already
                if self.slots[index] != value:
                    self._size += 1
                self.slots[index] = value  # type: ignore cannot assign str to None
                return index

    def find(self, value) -> int | None:
        index = self.hash_fun(value) % self.size
        for _ in range(self.size // self.step + 1):
            if self.slots[index] == value:
                return index
            index = (index + self.step) % self.size
        return None

    def __len__(self) -> int:
        return self._size
