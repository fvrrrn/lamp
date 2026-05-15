import unittest

from t09 import NativeDictionary
from t09_2 import BitDictionary, Just, Nothing, OrderedDictionary


class TestNativeDictionary(unittest.TestCase):
    def test_put_and_get(self):
        d = NativeDictionary[int](2)
        self.assertIsNone(d.get("key1"))
        d.put("key1", 42)
        self.assertEqual(d.get("key1"), 42)

    def test_setitem_and_getitem(self):
        d = NativeDictionary[int](2)
        d["alpha"] = 100
        self.assertEqual(d["alpha"], 100)

    def test_is_key(self):
        d = NativeDictionary[int](2)
        self.assertFalse(d.is_key("missing"))
        d.put("exists", 1)
        self.assertTrue(d.is_key("exists"))

    def test_overwrite_value(self):
        d = NativeDictionary[int](2)
        d.put("key", 1)
        d.put("key", 99)
        self.assertEqual(d.get("key"), 99)
        self.assertEqual(len(d), 1)  # size shouldn't increase

    def test_len_tracking(self):
        d = NativeDictionary[int](2)
        self.assertEqual(len(d), 0)
        d.put("k1", 1)
        d.put("k2", 2)
        self.assertEqual(len(d), 2)

    def test_setitem(self):
        d = NativeDictionary[int](2)
        d["k1"] = 1
        d["k2"] = 2
        self.assertEqual(len(d), 2)

    def test_getitem(self):
        d = NativeDictionary[int](2)
        d["k1"] = 1
        d["k2"] = 2
        self.assertEqual(1, d["k1"])
        self.assertEqual(2, d["k2"])

    def test_nonexistent_key(self):
        d = NativeDictionary[int](2)
        self.assertIsNone(d.get("ghost"))
        self.assertFalse(d.is_key("ghost"))


class TestOrderedDictionary(unittest.TestCase):
    def test_insert_and_get(self):
        d = OrderedDictionary[str, int]()
        self.assertEqual(d["a"], Nothing())
        self.assertEqual(len(d), 0)

        self.assertEqual(d.__setitem__("b", 2), Nothing())
        self.assertEqual(len(d), 1)
        self.assertEqual(d["b"], Just(2))

        d["a"] = 1
        d["c"] = 3
        self.assertEqual(len(d), 3)
        self.assertEqual(d["a"], Just(1))
        self.assertEqual(d["c"], Just(3))

        self.assertEqual(d.__setitem__("a", 10), Just(2))
        self.assertEqual(d["a"], Just(10))

    def test_contains(self):
        d = OrderedDictionary[str, int]()
        d["foo"] = 42
        d["bar"] = 99
        self.assertTrue("foo" in d)
        self.assertTrue("bar" in d)
        self.assertFalse("baz" in d)

    def test_str(self):
        d = OrderedDictionary[str, int]()
        d["x"] = 1
        d["y"] = 2
        s = str(d)
        self.assertIn("x", s)
        self.assertIn("y", s)


class TestBitDictionary(unittest.TestCase):
    def test_put_and_get(self):
        d = BitDictionary[int]()
        d.put("101", 42)
        d.put("111", 84)
        self.assertEqual(d.get("101"), 42)
        self.assertEqual(d.get("111"), 84)
        self.assertIsNone(d.get("000"))

    def test_setitem_getitem(self):
        d = BitDictionary[int]()
        d["000"] = 100
        d["001"] = 200
        self.assertEqual(d["000"], 100)
        self.assertEqual(d["001"], 200)
        self.assertIsNone(d["010"])

    def test_replacement(self):
        d = BitDictionary[int]()
        d["001"] = 1
        d["001"] = 2
        self.assertEqual(d["001"], 2)
        self.assertEqual(len(d), 1)

    def test_is_key(self):
        d = BitDictionary[int]()
        d["111"] = 5
        self.assertTrue(d.is_key("111"))
        self.assertFalse(d.is_key("000"))

    def test_len(self):
        d = BitDictionary[int]()
        self.assertEqual(len(d), 0)
        d["0"] = 1
        d["1"] = 2
        self.assertEqual(len(d), 2)
        d["1"] = 3
        self.assertEqual(len(d), 2)

    def test_del(self):
        d = BitDictionary[int]()
        d["key"] = 123
        self.assertEqual(d["key"], 123)
        del d["key"]
        self.assertIsNone(d["key"])
        self.assertEqual(len(d), 1)


if __name__ == "__main__":
    unittest.main()
