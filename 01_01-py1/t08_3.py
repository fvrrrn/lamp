import unittest

from t08 import HashTable
from t08_2 import DynHashTable, SaltedHashTable, generate_colliding_keys


class TestHashTable(unittest.TestCase):
    def test_hash_fun_consistency(self):
        ht = HashTable(sz=10, stp=1)
        val = "abc123"
        h1 = ht.hash_fun(val)
        h2 = ht.hash_fun(val)
        self.assertEqual(h1, h2, "hash_fun should return consistent results for same input")

    def test_hash_fun_different_strings(self):
        ht = HashTable(sz=10, stp=1)
        h1 = ht.hash_fun("abc")
        h2 = ht.hash_fun("abd")
        self.assertNotEqual(h1, h2, "hash_fun should return different values for different strings")

    def test_seek_slot_empty_table(self):
        ht = HashTable(sz=5, stp=1)
        index = ht.seek_slot("abc")
        self.assertIsNotNone(index)
        # type won't infer
        assert index is not None
        self.assertGreaterEqual(index, 0)
        self.assertLess(index, ht.size)

    def test_put_and_find_single_element(self):
        ht = HashTable(sz=10, stp=1)
        val = "test"
        idx_put = ht.put(val)
        self.assertIsNotNone(idx_put, "put should return an index for new element")
        idx_find = ht.find(val)
        self.assertEqual(idx_find, idx_put, "find should locate the element after put")

    def test_put_duplicate_value(self):
        ht = HashTable(sz=10, stp=1)
        val = "dup"
        idx1 = ht.put(val)
        idx2 = ht.put(val)
        self.assertEqual(idx1, idx2, "put of duplicate value should return same index")

    def test_find_nonexistent_value(self):
        ht = HashTable(sz=10, stp=1)
        ht.put("exists")
        idx = ht.find("missing")
        self.assertIsNone(idx, "find should return None for non-existent value")

    def test_put_until_full_and_fail(self):
        ht = HashTable(sz=3, stp=1)
        self.assertIsNotNone(ht.put("a"))
        self.assertIsNotNone(ht.put("b"))
        self.assertIsNotNone(ht.put("c"))
        idx = ht.put("d")
        self.assertIsNone(idx, "put should return None if table is full")

    def test_collision_resolution(self):
        ht = HashTable(sz=5, stp=1)
        val1 = "Aa"  # likely to produce specific hash
        val2 = "BB"
        idx1 = ht.put(val1)
        idx2 = ht.put(val2)
        self.assertIsNotNone(idx1)
        self.assertIsNotNone(idx2)
        self.assertNotEqual(idx1, idx2, "collision resolution should put values in different slots")
        self.assertEqual(ht.find(val1), idx1)
        self.assertEqual(ht.find(val2), idx2)

    def test_seek_slot_returns_none_when_full(self):
        ht = HashTable(sz=3, stp=1)
        ht.put("x")
        ht.put("y")
        ht.put("z")
        slot = ht.seek_slot("new")
        self.assertIsNone(slot, "seek_slot should return None if no slots available")

    def test_put_with_step_greater_than_one(self):
        ht = HashTable(sz=10, stp=3)
        val1 = "value1"
        val2 = "value2"
        idx1 = ht.put(val1)
        idx2 = ht.put(val2)
        self.assertIsNotNone(idx1)
        self.assertIsNotNone(idx2)
        self.assertNotEqual(idx1, idx2, "put should work correctly with step > 1")
        self.assertEqual(ht.find(val1), idx1)
        self.assertEqual(ht.find(val2), idx2)


class TestHashTable2(unittest.TestCase):
    def test_len_empty_table(self):
        ht = HashTable(sz=10, stp=1)
        self.assertEqual(len(ht), 0, "Empty table should have length 0")

    def test_len_after_one_put(self):
        ht = HashTable(sz=10, stp=1)
        ht.put("one")
        self.assertEqual(len(ht), 1, "Table should have length 1 after one insertion")

    def test_len_after_duplicate_put(self):
        ht = HashTable(sz=10, stp=1)
        ht.put("dup")
        ht.put("dup")
        self.assertEqual(len(ht), 1, "Inserting duplicate should not increase length")

    def test_len_after_duplicate_overflow(self):
        ht = HashTable(sz=2, stp=1)
        ht.put("dup")
        ht.put("dup")
        ht.put("dup")
        self.assertEqual(len(ht), 1, "Inserting duplicate overflow should not increase length")

    def test_len_after_multiple_puts(self):
        ht = HashTable(sz=10, stp=1)
        ht.put("a")
        ht.put("b")
        ht.put("c")
        self.assertEqual(len(ht), 3, "Table should count unique slots filled")

    def test_len_after_failed_put(self):
        ht = HashTable(sz=3, stp=1)
        ht.put("x")
        ht.put("y")
        ht.put("z")
        index = ht.put("overflow")
        self.assertIsNone(index)
        self.assertEqual(len(ht), 3, "Length should not change after failed insertion")

    def test_basic_put_and_find(self):
        ht = DynHashTable(8, 1)
        index = ht.put("apple")
        self.assertIsNotNone(index)
        self.assertEqual(ht.find("apple"), index)

    def test_duplicate_insertion(self):
        ht = DynHashTable(8, 1)
        index1 = ht.put("banana")
        index2 = ht.put("banana")
        self.assertEqual(index1, index2)
        self.assertEqual(len(ht), 1)

    def test_collision_and_probing(self):
        ht = DynHashTable(4, 1)
        # Manually create a collision by adding different keys
        ht.put("key1")
        ht.put("key2")
        ht.put("key3")
        self.assertEqual(len(ht), 3)

    def test_auto_resize(self):
        ht = DynHashTable(4, 1)
        keys = ["a", "b", "c", "d"]
        for key in keys:
            ht.put(key)
        # This insert should trigger a resize (load factor > 0.75)
        ht.put("e")
        self.assertGreater(ht.size, 4)
        self.assertEqual(len(ht), 5)
        for key in [*keys, "e"]:
            self.assertIsNotNone(ht.find(key))

    def test_resize_preserves_elements(self):
        ht = DynHashTable(2, 1)
        original_keys = [f"val{i}" for i in range(10)]
        for key in original_keys:
            ht.put(key)
        self.assertGreater(ht.size, 2)
        self.assertEqual(len(ht), len(original_keys))
        for key in original_keys:
            self.assertIsNotNone(ht.find(key))


class TestDDoSAttack(unittest.TestCase):
    def test_colliding_keys_all_land_in_same_slot(self):
        hash_table = HashTable(sz=17, stp=3)
        target_slot = 5
        colliding_keys = generate_colliding_keys(hash_table, target_slot, count=10)
        self.assertEqual(len(colliding_keys), 10)
        for key in colliding_keys:
            self.assertEqual(hash_table.hash_fun(key) % hash_table.size, target_slot)

    def test_collisions_degrade_performance(self):
        hash_table = HashTable(sz=17, stp=1)
        target_slot = 0
        colliding_keys = generate_colliding_keys(hash_table, target_slot, count=17)
        # fill the entire table with keys that all want slot 0
        for key in colliding_keys:
            hash_table.put(key)
        # all 17 slots occupied by keys that originally hash to slot 0
        self.assertEqual(len(hash_table), 17)
        # every slot is filled, table is completely jammed
        self.assertIsNone(hash_table.put("one_more"))

    def test_salted_table_resists_precomputed_collisions(self):
        # generate colliding keys for an unsalted table
        unsalted_table = HashTable(sz=17, stp=3)
        target_slot = 7
        colliding_keys = generate_colliding_keys(unsalted_table, target_slot, count=10)
        # verify they all collide in the unsalted table
        for key in colliding_keys:
            self.assertEqual(
                unsalted_table.hash_fun(key) % unsalted_table.size, target_slot
            )
        # now put them in a salted table -- salt randomises the hash,
        # so the precomputed keys should scatter across different slots
        salted_table = SaltedHashTable(sz=17, stp=3)
        occupied_slots = set()
        for key in colliding_keys:
            slot = salted_table.hash_fun(key) % salted_table.size
            occupied_slots.add(slot)
        # with 10 keys and 17 slots, random distribution should hit > 1 slot
        # (probability of all 10 landing in same slot is (1/17)^9 ~ 0)
        self.assertGreater(len(occupied_slots), 1)

    def test_two_salted_tables_give_different_hashes(self):
        table_first = SaltedHashTable(sz=17, stp=1)
        table_second = SaltedHashTable(sz=17, stp=1)
        test_value = "same_string"
        hash_first = table_first.hash_fun(test_value)
        hash_second = table_second.hash_fun(test_value)
        # different salt -> (almost certainly) different hash
        self.assertNotEqual(hash_first, hash_second)


if __name__ == "__main__":
    unittest.main()
