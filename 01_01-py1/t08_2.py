# TASK: 1.8.3
# TITLE: __len__ for HashTable
# TIME COMPLEXITY: O(1)
# SPACE COMPLEXITY: O(1)
# REFLECTION:
#     Just track counter in put(). Increment only when slot was empty before.
# Implementation is in t08.py HashTable.__len__


# TASK: 1.8.4*
# TITLE: Dynamic hash table that doubles size when load factor exceeds 75%
# TIME COMPLEXITY: put O(1) amortized, resize O(n)
# SPACE COMPLEXITY: O(n)
# REFLECTION:
#     Same idea as dynamic array: when table is too full, double the size
#     and rehash everything. Amortized cost stays O(1) per put because
#     resize happens rarely. Important to rehash all existing values
#     because hash_fun(value) % size changes when size changes.
from random import randint

from t08 import HashTable


class DynHashTable(HashTable):
    def __init__(self, sz, stp):
        super().__init__(sz, stp)

    def put(self, value: str) -> int | None:
        if self._size / self.size >= 0.75:
            self.__resize()
        return super().put(value)

    def __resize(self):
        old_slots = [slot for slot in self.slots if slot is not None]
        self.size *= 2
        self.slots = [None] * self.size
        self._size = 0
        for value in old_slots:
            super().put(value)


# TASK: 1.8.5*
# TITLE: DDoS attack on hash table via collision generation, then mitigate with salt
# TIME COMPLEXITY: --
# SPACE COMPLEXITY: --
# REFLECTION:
#     If attacker knows the hash function, they can precompute keys that all
#     map to same slot turning every put/find into O(n).
#     Adding random salt to hash input makes it close to impossible to predict
#     collisions from outside, because salt is generated at table creation
#     and never exposed. Even same value gives different hash in different
#     table instances
def generate_colliding_keys(hash_table: HashTable, target_slot: int, count: int) -> list[str]:
    colliding_keys: list[str] = []
    candidate_index = 0
    while len(colliding_keys) < count:
        candidate_key = f"attack_{candidate_index}"
        if hash_table.hash_fun(candidate_key) % hash_table.size == target_slot:
            colliding_keys.append(candidate_key)
        candidate_index += 1
    return colliding_keys


class SaltedHashTable(HashTable):
    def __init__(self, sz, stp):
        super().__init__(sz, stp)
        self.__salt = str(randint(0, 2**64))

    def hash_fun(self, value: str) -> int:
        return super().hash_fun(self.__salt + value)
