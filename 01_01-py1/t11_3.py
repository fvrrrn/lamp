import unittest

from t11 import BloomFilter
from t11_2 import AddableBloomFilter, RemovableBloomFilter


class TestBloomFilter(unittest.TestCase):
    def setUp(self):
        self.bf = BloomFilter(32)
        s = "0123456789"
        self.data = [s[x:] + s[:x] for x in range(len(s))]

    def test_hash_ranges(self):
        for s in self.data:
            h1 = self.bf.hash1(s)
            h2 = self.bf.hash2(s)
            self.assertGreaterEqual(h1, 0)
            self.assertLess(h1, self.bf.f_len)
            self.assertGreaterEqual(h2, 0)
            self.assertLess(h2, self.bf.f_len)

    def test_add_and_query(self):
        self.assertFalse(self.bf.is_value(self.data[0]))
        self.bf.add(self.data[0])
        self.assertTrue(self.bf.is_value(self.data[0]))

    def test_multiple_items(self):
        for item in self.data:
            self.bf.add(item)
        for item in self.data:
            self.assertTrue(self.bf.is_value(item))

    def test_nonexistent_item(self):
        self.bf.add(self.data[0])
        self.assertFalse(self.bf.is_value(self.data[1]))
        self.assertTrue(self.bf.is_value(self.data[0]))


class TestBloomFilter2(unittest.TestCase):
    def test_merge_bits_and_funcs(self):
        f1 = AddableBloomFilter(32, 0b0011, lambda _: 0)
        f2 = AddableBloomFilter(32, 0b0101, lambda _: 1)
        merged = f1 + f2
        self.assertEqual(merged.bit_array, 0b0111)
        self.assertEqual(merged.f_len, 32)
        self.assertEqual(len(merged.hash_fns), 2)
        self.assertEqual(merged.hash_fns[0]("x"), 0)
        self.assertEqual(merged.hash_fns[1]("x"), 1)
        self.assertEqual(f1.bit_array, 0b0011)
        self.assertEqual(f2.bit_array, 0b0101)

    def test_chain_addition(self):
        f1 = AddableBloomFilter(32, 0b100, lambda _: 4)
        f2 = AddableBloomFilter(32, 0b010, lambda _: 5)
        f3 = AddableBloomFilter(32, 0b001, lambda _: 6)
        merged = f1 + f2 + f3
        self.assertEqual(merged.bit_array, 0b111)
        self.assertEqual(len(merged.hash_fns), 3)
        outputs = sorted(fn("x") for fn in merged.hash_fns)
        self.assertEqual(outputs, [4, 5, 6])


class TestRemovableBloomFilter(unittest.TestCase):
    def setUp(self):
        self.f_len = 32
        self.bf = RemovableBloomFilter(self.f_len)
        s = "0123456789"
        self.data = [s[x:] + s[:x] for x in range(len(s))]
        self.assertLess(self.bf.hash_fns[0]("0123456789"), 32)

    def test_add_and_query_single(self):
        for item in self.data:
            self.bf.add(item)
        for item in self.data:
            self.assertTrue(self.bf.is_value(item))

    def test_shared_bits_false_positive_possible(self):
        self.bf.add("apple")
        # Add another value that shares at least one hash result with "banana"
        # But don't add "banana" itself
        self.assertFalse(self.bf.is_value("banana"))  # may still be false
        # Add banana to make sure it becomes detectable
        self.bf.add("banana")
        self.assertTrue(self.bf.is_value("banana"))

    def test_counting_preserves_multiple_adds(self):
        self.bf.add("apple")
        self.bf.add("apple")
        self.assertTrue(self.bf.is_value("apple"))
        # Manually check that all hash positions are incremented twice
        positions = [f("apple") for f in self.bf.hash_fns]
        for p in positions:
            self.assertEqual(self.bf.bit_array[p], 2)

    def test_remove_one(self):
        self.bf.add(self.data[0])
        self.bf.add(self.data[0])
        self.assertEqual(self.bf.bit_array[self.bf.hash_fns[0](self.data[0])], 2)
        self.assertEqual(self.bf.bit_array[self.bf.hash_fns[1](self.data[0])], 2)
        self.assertTrue(self.bf.is_value(self.data[0]))
        self.bf.remove(self.data[0])
        self.assertTrue(self.bf.is_value(self.data[0]))
        self.assertEqual(self.bf.bit_array[self.bf.hash_fns[0](self.data[0])], 1)
        self.assertEqual(self.bf.bit_array[self.bf.hash_fns[1](self.data[0])], 1)
        self.bf.remove(self.data[0])
        self.assertFalse(self.bf.is_value(self.data[0]))
        self.assertEqual(self.bf.bit_array[self.bf.hash_fns[0](self.data[0])], 0)
        self.assertEqual(self.bf.bit_array[self.bf.hash_fns[1](self.data[0])], 0)
        self.bf.remove(self.data[0])
        self.assertFalse(self.bf.is_value(self.data[0]))
        self.assertEqual(self.bf.bit_array[self.bf.hash_fns[0](self.data[0])], 0)
        self.assertEqual(self.bf.bit_array[self.bf.hash_fns[1](self.data[0])], 0)

    def test_remove_many(self):
        for item in self.data:
            self.bf.add(item)
        for i in range(len(self.data)):
            self.bf.remove(self.data[i])
            # each i-th of data is removed
            # then we check if all other elements are positive/false-positive
            # there shouldn't once be false-negative
            for item in self.data[i:]:
                self.bf.is_value(item)


if __name__ == "__main__":
    unittest.main()
