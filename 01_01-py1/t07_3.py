import unittest

from t07 import OrderedList, OrderedStringList
from t07_2 import OrderedDynArray, merge_ordered_lists, most_common, remove_duplicates


class TestOrderedList(unittest.TestCase):
    def test_add_ascending_order(self):
        ol = OrderedList(asc=True)
        ol.add(5)
        ol.add(3)
        ol.add(4)
        ol.add(1)
        ol.add(2)
        result = list(ol)
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_add_descending_order(self):
        ol = OrderedList(asc=False)
        ol.add(1)
        ol.add(3)
        ol.add(2)
        ol.add(5)
        ol.add(4)
        result = list(ol)
        self.assertEqual(result, [5, 4, 3, 2, 1])

    def test_find_existing(self):
        ol = OrderedList(asc=True)
        ol.add(1)
        ol.add(2)
        ol.add(3)
        node = ol.find(2)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 2)  # type: ignore

    def test_find_nonexistent(self):
        ol = OrderedList(asc=True)
        ol.add(1)
        ol.add(3)
        self.assertIsNone(ol.find(5))

    def test_delete_existing(self):
        ol = OrderedList(asc=True)
        ol.add(1)
        ol.add(2)
        ol.add(3)
        ol.delete(2)
        result = list(ol)
        self.assertEqual(result, [1, 3])

    def test_delete_nonexistent(self):
        ol = OrderedList(asc=True)
        ol.add(1)
        ol.add(2)
        ol.delete(5)  # should do nothing
        result = list(ol)
        self.assertEqual(result, [1, 2])

    def test_len_method(self):
        ol = OrderedList(asc=True)
        self.assertEqual(len(ol), 0)
        ol.add(1)
        ol.add(2)
        self.assertEqual(len(ol), 2)
        ol.delete(1)
        self.assertEqual(len(ol), 1)
        ol.delete(2)
        self.assertEqual(len(ol), 0)

    def test_get_all(self):
        ol = OrderedList(asc=True)
        ol.add(2)
        ol.add(1)
        nodes = ol.get_all()
        values = [n.value for n in nodes]
        self.assertEqual(values, [1, 2])

    def test_forward_iteration(self):
        ol = OrderedList(asc=True)
        for x in [3, 1, 2]:
            ol.add(x)
        values = list(ol)
        self.assertEqual(values, [1, 2, 3])

    def test_reverse_iteration(self):
        ol = OrderedList(asc=True)
        for x in [1, 3, 2]:
            ol.add(x)
        values = [value for value in reversed(ol)]
        self.assertEqual(values, [3, 2, 1])

    def test_str_representation(self):
        ol = OrderedList(asc=True)
        ol.add(3)
        ol.add(1)
        ol.add(2)
        self.assertEqual(str(ol), "1 -> 2 -> 3")

    def test_empty_list_has_length_zero(self):
        ol = OrderedList(asc=True)
        self.assertEqual(len(ol), 0)

    def test_add_single_element(self):
        ol = OrderedList(asc=True)
        ol.add(5)
        elements = list(ol)
        self.assertEqual(elements, [5])
        self.assertEqual(len(elements), 1)

    def test_add_multiple_elements_ascending(self):
        ol = OrderedList(asc=False)
        ol.add(5)
        ol.add(3)
        ol.add(7)
        elements = list(ol)
        self.assertEqual(elements, [7, 5, 3])  # based on your logic: highest first

    def test_add_multiple_elements_descending(self):
        ol = OrderedList(asc=False)
        ol.add(5)
        ol.add(3)
        ol.add(7)
        elements = list(ol)
        self.assertEqual(elements, [7, 5, 3])  # Same result unless add() logic flips for descending

    def test_find_existing_element(self):
        ol = OrderedList(asc=True)
        ol.add(1)
        ol.add(2)
        ol.add(3)
        node = ol.find(2)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 2)  # type: ignore

    def test_find_non_existing_element(self):
        ol = OrderedList(asc=True)
        ol.add(1)
        ol.add(2)
        node = ol.find(5)
        self.assertIsNone(node)

    def test_iterator_protocol(self):
        ol = OrderedList(asc=True)
        for value in [10, 20, 15]:
            ol.add(value)
        iterated = [x for x in ol]
        self.assertTrue(all(isinstance(i, int) for i in iterated))

    def test_string_representation(self):
        ol = OrderedList(asc=False)
        ol.add(1)
        ol.add(2)
        ol.add(3)
        expected = "3 -> 2 -> 1"
        self.assertEqual(str(ol), expected)

    def test_delete_existing_element(self):
        ol = OrderedList(asc=False)
        ol.add(3)
        ol.add(2)
        ol.add(1)
        ol.delete(2)
        elements = list(ol)
        self.assertEqual(elements, [3, 1])  # 2 is removed

    def test_delete_non_existing_element(self):
        ol = OrderedList(asc=False)
        ol.add(1)
        ol.add(2)
        ol.delete(5)  # No exception should be raised
        elements = list(ol)
        self.assertEqual(elements, [2, 1])  # List unchanged

    def test_delete_from_empty_list(self):
        ol = OrderedList(asc=True)
        ol.delete(10)  # No exception should be raised
        elements = list(ol)
        self.assertEqual(elements, [])  # Still empty

    def test_delete_all_elements(self):
        ol = OrderedList(asc=True)
        ol.add(1)
        ol.add(2)
        ol.add(3)
        ol.delete(1)
        ol.delete(2)
        ol.delete(3)
        self.assertEqual(list(ol), [])  # List is empty after deletions

    def test_delete_duplicate_element_once(self):
        ol = OrderedList(asc=True)
        ol.add(1)
        ol.add(2)
        ol.add(2)
        ol.delete(2)
        elements = list(ol)
        self.assertEqual(elements.count(2), 1)  # Only one 2 remains


class TestOrderedStringList(unittest.TestCase):
    def test_add_strings_preserves_spaces(self):
        osl = OrderedStringList(asc=True)
        osl.add("  banana ")
        osl.add("apple")
        osl.add("  cherry")
        result = list(osl)
        # Should be sorted using stripped values, but keep original strings
        self.assertEqual(result, ["apple", "  banana ", "  cherry"])

    def test_add_strings_descending_order(self):
        osl = OrderedStringList(asc=False)
        osl.add("  banana ")
        osl.add("apple")
        osl.add("  cherry")
        result = list(osl)
        self.assertEqual(result, ["  cherry", "  banana ", "apple"])

    def test_add_duplicate_strings_with_spaces(self):
        osl = OrderedStringList(asc=True)
        osl.add("wolf")
        osl.add("  wolf ")
        result = list(osl)
        # for the first implementation add early
        # self.assertEqual(result, ["wolf", "  wolf "])
        self.assertEqual(result, ["  wolf ", "wolf"])

    def test_str_representation_keeps_spaces(self):
        osl = OrderedStringList(asc=True)
        osl.add("  x ")
        osl.add("a")
        self.assertEqual(str(osl), "a ->   x ")


class TestOrderedList2(unittest.TestCase):
    def test_t7_8(self):
        ol = OrderedList(asc=False)
        deduped = remove_duplicates(ol)
        result = list(deduped)
        self.assertEqual(result, [])

        ol = OrderedList(False, 1)
        deduped = remove_duplicates(ol)
        result = list(deduped)
        self.assertEqual(result, [1])

        ol = OrderedList(asc=False)
        for val in [5, 5, 4, 4, 3, 2, 2, 1]:
            ol.add(val)
        deduped = remove_duplicates(ol)
        result = list(deduped)
        self.assertEqual(result, [5, 4, 3, 2, 1])

        ol = OrderedList(asc=True)
        for val in [1, 1, 2, 2, 2, 3, 4, 4, 5]:
            ol.add(val)

        deduped = remove_duplicates(ol)
        result = list(deduped)

        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_merge_both_nonempty_ascending(self):
        ol1 = OrderedList(asc=True)
        ol2 = OrderedList(asc=True)
        for val in [1, 3, 5]:
            ol1.add(val)
        for val in [2, 4, 6]:
            ol2.add(val)

        merged = merge_ordered_lists(ol1, ol2, asc=True)
        result = list(merged)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])

    def test_merge_both_nonempty_descending(self):
        ol1 = OrderedList(asc=False)
        ol2 = OrderedList(asc=False)
        for val in [5, 3, 1]:
            ol1.add(val)
        for val in [6, 4, 2]:
            ol2.add(val)

        merged = merge_ordered_lists(ol1, ol2, asc=False)
        result = list(merged)
        self.assertEqual(result, [6, 5, 4, 3, 2, 1])

    def test_merge_both_nonempty_ascending_descending(self):
        ol1 = OrderedList(asc=False)
        ol2 = OrderedList(asc=True)
        for val in [5, 3, 1]:
            ol1.add(val)
        for val in [1, 2, 3]:
            ol2.add(val)

        merged = merge_ordered_lists(ol1, ol2, asc=True)
        result = list(merged)
        self.assertEqual(result, [1, 1, 2, 3, 3, 5])

    def test_merge_one_empty(self):
        ol1 = OrderedList(asc=True)
        ol2 = OrderedList(asc=True)
        for val in [1, 2, 3]:
            ol1.add(val)
        # ol2 remains empty

        merged = merge_ordered_lists(ol1, ol2, asc=True)
        result = list(merged)
        self.assertEqual(result, [1, 2, 3])

    def test_merge_both_empty(self):
        ol1 = OrderedList(asc=True)
        ol2 = OrderedList(asc=True)
        merged = merge_ordered_lists(ol1, ol2, asc=True)
        result = list(merged)
        self.assertEqual(result, [])

    def test_merge_duplicates(self):
        ol1 = OrderedList(asc=True)
        ol2 = OrderedList(asc=True)
        for val in [1, 2, 3]:
            ol1.add(val)
        for val in [2, 3, 4]:
            ol2.add(val)

        merged = merge_ordered_lists(ol1, ol2, asc=True)
        result = list(merged)
        self.assertEqual(result, [1, 2, 2, 3, 3, 4])

    def test_empty_sublist(self):
        main = OrderedList(asc=True)
        for v in [1, 2, 3]:
            main.add(v)

        sub = OrderedList(asc=True)
        self.assertTrue(sub in main)

    def test_exact_match(self):
        main = OrderedList(asc=True)
        for v in [1, 2, 3]:
            main.add(v)

        sub = OrderedList(asc=True)
        for v in [1, 2, 3]:
            sub.add(v)

        self.assertTrue(sub in main)

    def test_sublist_match_middle(self):
        main = OrderedList(asc=True)
        for v in [1, 2, 3, 4, 5]:
            main.add(v)

        sub = OrderedList(asc=True)
        for v in [3, 4]:
            sub.add(v)

        self.assertTrue(sub in main)

    def test_sublist_not_present(self):
        main = OrderedList(asc=True)
        for v in [1, 2, 3, 4, 5]:
            main.add(v)

        sub = OrderedList(asc=True)
        for v in [2, 4]:
            sub.add(v)

        self.assertFalse(sub in main)

    def test_sublist_larger_than_main(self):
        main = OrderedList(asc=True)
        for v in [1, 2]:
            main.add(v)

        sub = OrderedList(asc=True)
        for v in [1, 2, 3]:
            sub.add(v)

        self.assertFalse(sub in main)

    def test_empty_main_non_empty_sub(self):
        main = OrderedList(asc=True)

        sub = OrderedList(asc=True)
        sub.add(1)

        self.assertFalse(sub in main)

    def test_direction_mismatch(self):
        main = OrderedList(asc=True)
        for v in [1, 2, 3, 4, 5]:
            main.add(v)

        sub = OrderedList(asc=False)
        for v in [3, 2]:
            sub.add(v)

        self.assertFalse(sub in main)

    def test_descending_contains(self):
        main = OrderedList(asc=False)
        for v in [5, 4, 3, 2, 1]:
            main.add(v)

        sub = OrderedList(asc=False)
        for v in [4, 3, 2]:
            sub.add(v)

        self.assertTrue(sub in main)

    def test_empty_ordered_list(self):
        ol = OrderedList(asc=True)
        self.assertIsNone(most_common(ol))

    def test_single_element(self):
        ol = OrderedList(asc=True)
        ol.add(42)
        self.assertEqual(most_common(ol), 42)

    def test_multiple_unique_elements(self):
        ol = OrderedList(asc=True)
        for v in [1, 2, 3, 4, 5]:
            ol.add(v)
        self.assertIn(most_common(ol), [1, 2, 3, 4, 5])  # all appear once

    def test_clear_most_common(self):
        ol = OrderedList(asc=True)
        for v in [1, 2, 2, 3, 3, 3, 4]:
            ol.add(v)
        self.assertEqual(most_common(ol), 3)

    def test_tie_returns_first_encountered(self):
        ol = OrderedList(asc=True)
        for v in [1, 2, 2, 3, 3]:
            ol.add(v)
        result = most_common(ol)
        self.assertIn(result, [2, 3])  # Either 2 or 3 is acceptable in a tie

    def test_descending_order(self):
        ol = OrderedList(asc=False)
        for v in [5, 4, 4, 3, 2]:
            ol.add(v)
        self.assertEqual(most_common(ol), 4)

    def test_add_ascending(self):
        arr = OrderedDynArray[int](asc=True)
        for val in [5, 1, 3, 2, 4]:
            arr.add(val)
        self.assertEqual(list(arr), [1, 2, 3, 4, 5])

    def test_add_descending(self):
        arr = OrderedDynArray[int](asc=False)
        for val in [2, 4, 1, 3, 5]:
            arr.add(val)
        self.assertEqual(list(arr), [5, 4, 3, 2, 1])

    def test_find_existing_ascending(self):
        arr = OrderedDynArray[int](asc=True)
        for val in [3, 1, 4, 2]:
            arr.add(val)
        self.assertEqual(arr.find(1), 0)
        self.assertEqual(arr.find(3), 2)
        self.assertEqual(arr.find(4), 3)

    def test_find_existing_descending(self):
        arr = OrderedDynArray[int](asc=False)
        for val in [1, 3, 2, 4]:
            arr.add(val)
        self.assertEqual(arr.find(4), 0)
        self.assertEqual(arr.find(3), 1)
        self.assertEqual(arr.find(1), 3)

    def test_find_not_existing(self):
        arr = OrderedDynArray[int](asc=True)
        for val in [10, 20, 30]:
            arr.add(val)
        self.assertEqual(arr.find(25), -1)
        self.assertEqual(arr.find(5), -1)
        self.assertEqual(arr.find(100), -1)

    def test_empty_find(self):
        arr = OrderedDynArray[int](asc=True)
        self.assertEqual(arr.find(1), -1)

    def test_add_duplicates(self):
        arr = OrderedDynArray[int](asc=True)
        for val in [2, 1, 2, 3, 2]:
            arr.add(val)
        self.assertEqual(list(arr), [1, 2, 2, 2, 3])
        self.assertIn(arr.find(2), [1, 2, 3])  # any of the 2s is acceptable


if __name__ == "__main__":
    unittest.main()
