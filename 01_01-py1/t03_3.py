import unittest

from t03 import DynArray
from t03_2 import DynArray2, MultiDynArray


class TestDynArrayMethods(unittest.TestCase):
    def setUp(self):
        self.array = DynArray()

    def test_insert_no_buffer_increase(self):
        for i in range(15):
            self.array.insert(i, i)
        self.assertEqual(len(self.array), 15)
        self.assertEqual(self.array.capacity, 16)
        self.array.insert(15, 99)
        self.assertEqual(len(self.array), 16)
        self.assertEqual(self.array.capacity, 16)
        self.assertEqual(self.array[15], 99)

    def test_insert_with_buffer_increase(self):
        for i in range(16):
            self.array.insert(i, i)
        self.array.insert(16, 99)
        self.assertEqual(len(self.array), 17)
        self.assertGreater(self.array.capacity, 16)
        self.assertEqual(self.array[16], 99)

    def test_insert_invalid_position(self):
        with self.assertRaises(IndexError):
            self.array.insert(-1, 5)
        with self.assertRaises(IndexError):
            self.array.insert(100, 5)

    def test_delete_no_buffer_decrease(self):
        for i in range(16):
            self.array.insert(i, i)
        self.array.delete(15)
        self.assertEqual(len(self.array), 15)
        self.assertEqual(self.array.capacity, 16)

    def test_delete_with_buffer_decrease(self):
        for i in range(32):
            self.array.insert(i, i)
        for _ in range(25):
            self.array.delete(len(self.array) - 1)
        self.assertEqual(len(self.array), 7)
        self.assertLess(self.array.capacity, 32)

    def test_delete_invalid_position(self):
        with self.assertRaises(IndexError):
            self.array.delete(-1)
        with self.assertRaises(IndexError):
            self.array.delete(100)


class TestDynArray2(unittest.TestCase):
    def setUp(self):
        self.arr: DynArray2[int] = DynArray2()

    def _items(self) -> list[int]:
        return [self.arr[i] for i in range(len(self.arr))]

    # -- initial state --

    def test_initial_state(self):
        self.assertEqual(len(self.arr), 0)
        self.assertEqual(self.arr.capacity, 16)
        self.assertEqual(self.arr.bank, 0)

    # -- append / bank --

    def test_append_increments_count_and_bank(self):
        self.arr.append(1)
        self.assertEqual(len(self.arr), 1)
        self.assertEqual(self.arr.bank, 2)
        self.assertEqual(self.arr[0], 1)

    def test_append_bank_accumulates(self):
        for i in range(5):
            self.arr.append(i)
        self.assertEqual(self.arr.bank, 10)

    def test_append_fills_capacity_without_resize(self):
        for i in range(16):
            self.arr.append(i)
        self.assertEqual(len(self.arr), 16)
        self.assertEqual(self.arr.capacity, 16)
        self.assertEqual(self.arr.bank, 32)

    def test_append_beyond_capacity_doubles_it(self):
        for i in range(17):
            self.arr.append(i)
        self.assertEqual(len(self.arr), 17)
        self.assertEqual(self.arr.capacity, 32)

    def test_append_resize_deducts_bank(self):
        for i in range(17):
            self.arr.append(i)
        # bank: 17*2=34 deposited, 16 withdrawn on resize -> 18
        self.assertEqual(self.arr.bank, 18)

    def test_append_preserves_values_after_resize(self):
        for i in range(17):
            self.arr.append(i)
        self.assertEqual(self._items(), list(range(17)))

    # -- resize guard --

    def test_resize_raises_if_bank_insufficient(self):
        self.arr.count = 10
        self.arr.bank = 5  # 5 < 10
        with self.assertRaises(RuntimeError):
            self.arr.resize(32)

    # -- insert --

    def test_insert_at_beginning(self):
        self.arr.append(2)
        self.arr.append(3)
        self.arr.insert(0, 1)
        self.assertEqual(self._items(), [1, 2, 3])

    def test_insert_in_middle(self):
        self.arr.append(1)
        self.arr.append(3)
        self.arr.insert(1, 2)
        self.assertEqual(self._items(), [1, 2, 3])

    def test_insert_at_end(self):
        self.arr.append(1)
        self.arr.append(2)
        self.arr.insert(2, 3)
        self.assertEqual(self._items(), [1, 2, 3])

    def test_insert_deposits_bank(self):
        self.arr.insert(0, 99)
        self.assertEqual(self.arr.bank, 2)

    def test_insert_negative_index_raises(self):
        with self.assertRaises(IndexError):
            self.arr.insert(-1, 5)

    def test_insert_beyond_count_raises(self):
        self.arr.append(1)
        with self.assertRaises(IndexError):
            self.arr.insert(2, 5)

    def test_insert_triggers_resize(self):
        for i in range(16):
            self.arr.append(i)
        self.arr.insert(0, 99)
        self.assertEqual(len(self.arr), 17)
        self.assertEqual(self.arr.capacity, 32)
        self.assertEqual(self.arr[0], 99)

    # -- getitem bounds --

    def test_getitem_negative_raises(self):
        self.arr.append(1)
        with self.assertRaises(IndexError):
            _ = self.arr[-1]

    def test_getitem_beyond_count_raises(self):
        with self.assertRaises(IndexError):
            _ = self.arr[0]


class TestMultiDynArray(unittest.TestCase):
    # -- init --

    def test_empty_level_raises(self):
        with self.assertRaises(ValueError):
            MultiDynArray([])

    def test_1d_init_all_none(self):
        ma = MultiDynArray([3])
        self.assertEqual(ma.dim, 1)
        for i in range(3):
            self.assertIsNone(ma[[i]])

    def test_2d_init_all_none(self):
        ma = MultiDynArray([2, 3])
        self.assertEqual(ma.dim, 2)
        for row in range(2):
            for col in range(3):
                self.assertIsNone(ma[[row, col]])

    # -- getitem --

    def test_getitem_wrong_dim_raises(self):
        ma = MultiDynArray([2, 3])
        with self.assertRaises(IndexError):
            _ = ma[[0]]

    def test_getitem_out_of_bounds_raises(self):
        ma = MultiDynArray([2, 3])
        with self.assertRaises(IndexError):
            _ = ma[[5, 0]]

    def test_getitem_negative_raises(self):
        ma = MultiDynArray([3])
        with self.assertRaises(IndexError):
            _ = ma[[-1]]

    # -- setitem / roundtrip --

    def test_setitem_getitem_1d(self):
        ma = MultiDynArray([3])
        ma[[1]] = 42
        self.assertEqual(ma[[1]], 42)
        self.assertIsNone(ma[[0]])

    def test_setitem_getitem_2d(self):
        ma = MultiDynArray([2, 3])
        ma[[1, 2]] = "hello"
        self.assertEqual(ma[[1, 2]], "hello")
        self.assertIsNone(ma[[0, 0]])

    def test_setitem_negative_index_raises(self):
        ma = MultiDynArray([3])
        with self.assertRaises(IndexError):
            ma[[-1]] = 99

    def test_setitem_wrong_dim_raises(self):
        ma = MultiDynArray([2, 3])
        with self.assertRaises(IndexError):
            ma[[0]] = 99

    def test_setitem_extends_beyond_initial_size(self):
        ma = MultiDynArray([2])
        ma[[5]] = 77
        self.assertEqual(ma[[5]], 77)
        self.assertIsNone(ma[[3]])

    def test_setitem_extends_2d_row(self):
        ma = MultiDynArray([2, 2])
        ma[[4, 1]] = "x"
        self.assertEqual(ma[[4, 1]], "x")


if __name__ == "__main__":
    unittest.main()
