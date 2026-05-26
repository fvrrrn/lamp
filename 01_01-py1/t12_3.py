import unittest

from t12 import Just, NativeCache, Nothing, polynomial_hash


class TestNativeCache(unittest.TestCase):
    def test_first_access_calls_getter(self):
        called_keys = []

        def getter(k: str) -> str:
            called_keys.append(k)
            return k.upper()

        cache = NativeCache[str, str](sz=5, getter=getter, hasher=polynomial_hash)
        maybe_result = cache["a"]
        match maybe_result:
            case Just(value):
                self.assertEqual(value, "A")
                self.assertIn("a", called_keys)
            case Nothing():
                self.fail("Expected Just, got Nothing")

    def test_second_access_uses_cache(self):
        calls = []

        def getter(k: str) -> str:
            calls.append(k)
            return k.upper()

        cache = NativeCache[str, str](sz=5, getter=getter, hasher=polynomial_hash)
        # call getter
        cache["b"]
        # should not call getter again
        maybe_result = cache["b"]
        match maybe_result:
            case Just(value):
                self.assertEqual(value, "B")
                self.assertEqual(len(calls), 1)
            case Nothing():
                self.fail("Expected Just, got Nothing")

    def test_access_count_increments(self):
        def getter(k: str) -> str:
            return k.upper()

        cache = NativeCache[str, str](sz=5, getter=getter, hasher=polynomial_hash)
        cache["x"]
        cache["x"]
        cache["x"]
        maybe_index = cache.dict.__contains__("x")
        match maybe_index:
            case Just(index):
                count = cache.hits[index]
                self.assertEqual(count, 2)
            case Nothing():
                self.fail("Expected Just(index), got Nothing")

    def test_multiple_keys_cached_separately(self):
        def getter(k: str) -> str:
            return k + "!"

        cache = NativeCache[str, str](sz=7, getter=getter, hasher=polynomial_hash)
        maybe_a = cache["a"]
        maybe_b = cache["b"]
        maybe_c = cache["c"]

        match maybe_a:
            case Just(value):
                self.assertEqual(value, "a!")
            case Nothing():
                self.fail("Expected Just, got Nothing")

        match maybe_b:
            case Just(value):
                self.assertEqual(value, "b!")
            case Nothing():
                self.fail("Expected Just, got Nothing")

        match maybe_c:
            case Just(value):
                self.assertEqual(value, "c!")
            case Nothing():
                self.fail("Expected Just, got Nothing")

        for key in ["a", "b", "c"]:
            match cache.dict.__contains__(key):
                case Just(index):
                    count = cache.hits[index]
                    self.assertEqual(count, 0)
                case Nothing():
                    self.fail(f"Expected Just(index) for key={key}, got Nothing")

    def test_cache_replacement(self):
        def getter(k: str) -> str:
            return k + "!"

        cache = NativeCache[str, str](sz=7, getter=getter, hasher=polynomial_hash)
        maybe_a = cache["a"]
        maybe_b = cache["b"]
        maybe_c = cache["c"]

        match maybe_a:
            case Just(value):
                self.assertEqual(value, "a!")
            case Nothing():
                self.fail("Expected Just, got Nothing")

        match maybe_b:
            case Just(value):
                self.assertEqual(value, "b!")
            case Nothing():
                self.fail("Expected Just, got Nothing")

        match maybe_c:
            case Just(value):
                self.assertEqual(value, "c!")
            case Nothing():
                self.fail("Expected Just, got Nothing")

        for key in ["a", "b", "c"]:
            match cache.dict.__contains__(key):
                case Just(index):
                    count = cache.hits[index]
                    self.assertEqual(count, 0)
                case Nothing():
                    self.fail(f"Expected Just(index) for key={key}, got Nothing")

    def test_eviction_replaces_least_used(self):
        inserted = []

        def getter(k: str) -> str:
            inserted.append(k)
            return k.upper()

        cache = NativeCache[str, str](2, getter, polynomial_hash)

        cache["a"]  # Insert 'A'
        cache["b"]  # Insert 'B'
        cache["c"]  # Cache is full, evict least-used: 'a' or 'b'

        slots = cache.dict.slots

        self.assertIn("c", slots)
        self.assertEqual(len([k for k in slots if k is not None]), 2)

    def test_least_accessed_eviction_logic(self):
        cache = NativeCache[str, str](2, lambda k: k.upper(), polynomial_hash)

        cache["x"]  # index0
        cache["y"]  # index1

        cache["x"]  # x gets 2 hits
        cache["x"]  # x gets 3 hits

        cache["z"]  # y has fewer hits therefore y should be evicted

        slots = cache.dict.slots
        self.assertIn("x", slots)
        self.assertIn("z", slots)
        self.assertNotIn("y", slots)


if __name__ == "__main__":
    unittest.main()
