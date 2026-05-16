import unittest

from t10 import PowerSet
from t10_2 import Bag


class TestPowerSet(unittest.TestCase):
    def test_put_and_get(self):
        s = PowerSet[str]()
        s.put("a")
        s.put("b")
        s.put("b")
        self.assertTrue("a" in s)
        self.assertTrue("b" in s)
        self.assertTrue(s.get("b"))
        self.assertFalse("c" in s)

    def test_remove(self):
        ps = PowerSet[int]()
        ps.put(42)
        self.assertTrue(ps.get(42))
        self.assertTrue(ps.remove(42))
        self.assertFalse(ps.get(42))
        self.assertFalse(ps.remove(42))

    def test_intersection(self):
        a = PowerSet()
        b = PowerSet()
        a.put("p")
        a.put("q")
        b.put("p")
        b.put("q")
        result = a.intersection(b)
        self.assertEqual(len(result), 2)
        self.assertIn("q", result)
        self.assertIn("p", result)

        result = PowerSet().intersection(PowerSet())
        self.assertEqual(len(result), 0)

        result = PowerSet(1, 2).intersection(PowerSet(3, 4))
        self.assertEqual(len(result), 0)
        self.assertNotIn(1, result)
        self.assertNotIn(2, result)
        self.assertNotIn(3, result)
        self.assertNotIn(4, result)

        result = PowerSet(1, 2).intersection(PowerSet())
        self.assertEqual(len(result), 0)
        self.assertNotIn(1, result)
        self.assertNotIn(2, result)

        result = PowerSet().intersection(PowerSet(3, 4))
        self.assertEqual(len(result), 0)
        self.assertNotIn(3, result)
        self.assertNotIn(4, result)

        a = PowerSet()
        b = PowerSet()
        for i in range(100000):
            a.put(i)
            b.put(i)
        self.assertEqual(a.intersection(b), a)
        self.assertEqual(a.intersection(b), b)
        self.assertEqual(b.intersection(a), a)
        self.assertEqual(b.intersection(a), b)

    def test_union(self):
        a = PowerSet()
        b = PowerSet()
        a.put("p")
        a.put("q")
        b.put("p")
        b.put("q")
        b.put("r")
        result = a.union(b)
        self.assertEqual(len(result), 3)
        self.assertIn("p", result)
        self.assertIn("q", result)
        self.assertIn("r", result)

        result = PowerSet().union(PowerSet())
        self.assertEqual(len(result), 0)

        result = PowerSet(1, 2).union(PowerSet(3, 4))
        self.assertEqual(len(result), 4)
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertIn(3, result)
        self.assertIn(4, result)

        result = PowerSet(1, 2).union(PowerSet())
        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertIn(2, result)

        result = PowerSet().union(PowerSet(3, 4))
        self.assertEqual(len(result), 2)
        self.assertIn(3, result)
        self.assertIn(4, result)

        a = PowerSet()
        b = PowerSet()
        for i in range(100000):
            a.put(i)
            b.put(i)
        self.assertEqual(a.union(b), a)
        self.assertEqual(a.union(b), b)
        self.assertEqual(b.union(a), a)
        self.assertEqual(b.union(a), b)

    def test_difference(self):
        a = PowerSet()
        b = PowerSet()
        a.put("p")
        a.put("q")
        b.put("p")
        b.put("q")
        result = a.difference(b)
        self.assertEqual(len(result), 0)
        self.assertNotIn("q", result)
        self.assertNotIn("p", result)

        result = PowerSet().difference(PowerSet())
        self.assertEqual(len(result), 0)

        result = PowerSet(1, 2).difference(PowerSet(3, 4))
        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertNotIn(3, result)
        self.assertNotIn(4, result)

        result = PowerSet(1, 2).difference(PowerSet())
        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertIn(2, result)

        result = PowerSet().difference(PowerSet(3, 4))
        self.assertEqual(len(result), 0)
        self.assertNotIn(3, result)
        self.assertNotIn(4, result)

        a = PowerSet()
        b = PowerSet()
        for i in range(100000):
            a.put(i)
            b.put(i)
        self.assertEqual(a.difference(b), PowerSet())
        self.assertEqual(b.difference(a), PowerSet())

    def test_issubset(self):
        a = PowerSet()
        b = PowerSet()
        a.put("p")
        a.put("q")
        b.put("p")
        b.put("q")
        self.assertTrue(a.issubset(b))
        self.assertTrue(b.issubset(a))
        b.put("r")
        self.assertTrue(b.issubset(a))
        self.assertFalse(a.issubset(b))

        self.assertTrue(PowerSet().issubset(PowerSet()))

        self.assertFalse(PowerSet(1, 2).issubset(PowerSet(3, 4)))
        self.assertFalse(PowerSet(1, 2).issubset(PowerSet(3, 4)))

        self.assertFalse(PowerSet().issubset(PowerSet(3, 4)))
        self.assertTrue(PowerSet(1, 2).issubset(PowerSet()))

        self.assertTrue(PowerSet(1, 2).issubset(PowerSet(1, 2)))
        self.assertTrue(PowerSet(1, 2, 3).issubset(PowerSet(1, 2)))
        self.assertFalse(PowerSet(1, 2).issubset(PowerSet(1, 2, 3)))

        a = PowerSet()
        b = PowerSet()
        for i in range(100000):
            a.put(i)
            b.put(i)
        self.assertTrue(a.issubset(b))
        self.assertTrue(b.issubset(a))

    def test_equals(self):
        a = PowerSet()
        b = PowerSet()
        a.put("p")
        a.put("q")
        b.put("p")
        b.put("q")
        self.assertTrue(a.issubset(b))
        self.assertTrue(b.issubset(a))
        b.put("r")
        self.assertTrue(b.issubset(a))
        self.assertFalse(a.issubset(b))

        self.assertTrue(PowerSet().issubset(PowerSet()))

        self.assertFalse(PowerSet(1, 2).issubset(PowerSet(3, 4)))
        self.assertFalse(PowerSet(1, 2).issubset(PowerSet(3, 4)))

        self.assertFalse(PowerSet().issubset(PowerSet(3, 4)))
        self.assertTrue(PowerSet(1, 2).issubset(PowerSet()))

        self.assertTrue(PowerSet(1, 2).issubset(PowerSet(1, 2)))

        a = PowerSet()
        b = PowerSet()
        for i in range(100000):
            a.put(i)
            b.put(i)
        self.assertEqual(a, b)

    def test_len(self):
        s = PowerSet()
        self.assertEqual(len(s), 0)
        s.put("a")
        self.assertEqual(len(s), 1)
        s.put("b")
        self.assertEqual(len(s), 2)
        s.remove("b")
        self.assertEqual(len(s), 1)
        s.remove("a")
        self.assertEqual(len(s), 0)

        a = PowerSet()
        for i in range(100000):
            a.put(i)
        self.assertEqual(len(a), 100000)


class TestBag(unittest.TestCase):
    def setUp(self):
        self.bag1 = Bag("a", "b", "b", "c")
        self.bag2 = Bag("b", "b", "c", "d")

    def test_put_and_get(self):
        self.bag1.put("d", 2)
        self.assertIn("d", self.bag1)
        self.assertEqual(self.bag1["d"], 2)

    def test_remove_and_delitem(self):
        self.assertTrue(self.bag1.remove("b"))
        self.assertTrue(self.bag1.remove("b"))
        self.assertFalse("b" in self.bag1)
        self.assertFalse(self.bag1.remove("b"))

    def test_intersection(self):
        result = self.bag1.intersection(self.bag2)
        self.assertEqual(result["b"], 2)
        self.assertEqual(result["c"], 1)
        self.assertNotIn("a", result)
        self.assertNotIn("d", result)

    def test_union(self):
        result = self.bag1.union(self.bag2)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"], 4)
        self.assertEqual(result["c"], 2)
        self.assertEqual(result["d"], 1)

    def test_difference(self):
        result = self.bag1.difference(self.bag2)
        self.assertEqual(result["a"], 1)
        self.assertNotIn("c", result)
        self.assertEqual(result["b"], 0)

    def test_issubset(self):
        bag3 = Bag("b", "c")
        self.assertFalse(bag3.issubset(self.bag2))
        self.assertTrue(self.bag2.issubset(bag3))

    def test_eq(self):
        bag1_copy = Bag("a", "b", "b", "c")
        self.assertEqual(self.bag1, bag1_copy)
        bag1_copy.put("c")
        self.assertNotEqual(self.bag1, bag1_copy)

    def test_multiple_intersection_common_elements(self):
        bag1 = Bag("a", "a", "b")
        bag2 = Bag("a", "a", "c")
        bag3 = Bag("a", "d")
        result = bag1.intersection(bag2, bag3)
        self.assertEqual(result, Bag("a"))

        bag1 = Bag("x", "y")
        bag2 = Bag("y", "z")
        bag3 = Bag("a", "b")
        result = bag1.intersection(bag2, bag3)
        self.assertEqual(result, Bag())

        bag1 = Bag("x", "x", "x", "y")
        bag2 = Bag("x", "x", "z")
        bag3 = Bag("x", "x", "x", "x")
        result = bag1.intersection(bag2, bag3)
        self.assertEqual(result, Bag("x", "x"))

        bag1 = Bag("a", "b", "c")
        bag2 = Bag("a", "b")
        bag3 = Bag()
        result = bag1.intersection(bag2, bag3)
        self.assertEqual(result, Bag())

        bag = Bag("a", "a", "b")
        result = bag.intersection(bag, bag, bag)
        self.assertEqual(result, Bag("a", "a", "b"))


if __name__ == "__main__":
    unittest.main()
