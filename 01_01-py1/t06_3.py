import unittest

from t06 import Deque
from t06_2 import MinDeque, is_balanced


class TestDeque(unittest.TestCase):
    def test_addFront_single_element(self):
        deque = Deque()
        deque.addFront(1)
        self.assertEqual(deque.size(), 1)
        self.assertEqual(deque.removeFront(), 1)
        self.assertEqual(deque.size(), 0)

    def test_addTail_single_element(self):
        deque = Deque()
        deque.addTail(1)
        self.assertEqual(deque.size(), 1)
        self.assertEqual(deque.removeTail(), 1)
        self.assertEqual(deque.size(), 0)

    def test_addFront_multiple_elements(self):
        deque = Deque()
        deque.addFront(1)
        deque.addFront(2)
        deque.addFront(3)
        self.assertEqual(deque.size(), 3)
        self.assertEqual(deque.removeFront(), 3)
        self.assertEqual(deque.removeFront(), 2)
        self.assertEqual(deque.removeFront(), 1)

    def test_addTail_multiple_elements(self):
        deque = Deque()
        deque.addTail(1)
        deque.addTail(2)
        deque.addTail(3)
        self.assertEqual(deque.size(), 3)
        self.assertEqual(deque.removeTail(), 3)
        self.assertEqual(deque.removeTail(), 2)
        self.assertEqual(deque.removeTail(), 1)

    def test_removeFront_empty_deque(self):
        deque = Deque()
        self.assertIsNone(deque.removeFront())

    def test_removeTail_empty_deque(self):
        deque = Deque()
        self.assertIsNone(deque.removeTail())

    def test_mixed_operations(self):
        deque = Deque()
        deque.addTail(1)
        deque.addFront(2)
        deque.addTail(3)
        deque.addFront(4)
        self.assertEqual(deque.size(), 4)
        self.assertEqual(deque.removeFront(), 4)
        self.assertEqual(deque.removeTail(), 3)
        self.assertEqual(deque.removeFront(), 2)
        self.assertEqual(deque.removeFront(), 1)
        self.assertEqual(deque.size(), 0)

    def test_iterator(self):
        deque = Deque()
        deque.addTail(1)
        deque.addTail(2)
        deque.addTail(3)
        elements = list(deque)
        self.assertEqual(elements, [1, 2, 3])

    def test_empty_deque_palindrome(self):
        dq = Deque[str]()
        self.assertTrue(dq.is_palindrome())

    def test_single_element(self):
        dq = Deque[str]()
        dq.addTail("a")
        self.assertTrue(dq.is_palindrome())

    def test_two_identical_elements(self):
        dq = Deque[str]()
        dq.addTail("a")
        dq.addTail("a")
        self.assertTrue(dq.is_palindrome())

    def test_two_different_elements(self):
        dq = Deque[str]()
        dq.addTail("a")
        dq.addTail("b")
        self.assertFalse(dq.is_palindrome())

    def test_even_length_palindrome(self):
        dq = Deque[str]()
        for char in "abba":
            dq.addTail(char)
        self.assertTrue(dq.is_palindrome())

    def test_even_length_non_palindrome(self):
        dq = Deque[str]()
        for char in "abca":
            dq.addTail(char)
        self.assertFalse(dq.is_palindrome())

    def test_odd_length_palindrome(self):
        dq = Deque[str]()
        for char in "racecar":
            dq.addTail(char)
        self.assertTrue(dq.is_palindrome())

    def test_odd_length_non_palindrome(self):
        dq = Deque[str]()
        for char in "hello":
            dq.addTail(char)
        self.assertFalse(dq.is_palindrome())

    def test_numeric_palindrome(self):
        dq = Deque[int]()
        for num in [1, 2, 3, 2, 1]:
            dq.addTail(num)
        self.assertTrue(dq.is_palindrome())

    def test_numeric_non_palindrome(self):
        dq = Deque[int]()
        for num in [1, 2, 3, 4, 5]:
            dq.addTail(num)
        self.assertFalse(dq.is_palindrome())

    def test_empty_deque(self):
        dq = MinDeque[int]()
        self.assertIsNone(dq._min)

    def test_add_single_element(self):
        dq = MinDeque[int]()
        dq.addTail(5)
        self.assertEqual(dq._min, 5)

    def test_add_multiple_elements(self):
        dq = MinDeque[int]()
        dq.addTail(5)
        dq.addTail(3)
        dq.addTail(7)
        self.assertEqual(dq._min, 3)

    def test_add_front_and_tail(self):
        dq = MinDeque[int]()
        dq.addTail(10)
        dq.addFront(5)
        dq.addTail(7)
        self.assertEqual(dq._min, 5)

    def test_remove_front(self):
        dq = MinDeque[int]()
        dq.addTail(10)
        dq.addTail(5)
        dq.addTail(7)
        self.assertEqual(dq._min, 5)

        dq.removeFront()  # Removes 10
        self.assertEqual(dq._min, 5)

        dq.removeFront()  # Removes 5
        self.assertEqual(dq._min, 7)

        dq.removeFront()  # Removes 7
        self.assertIsNone(dq._min)

    def test_remove_tail(self):
        dq = MinDeque[int]()
        dq.addTail(5)
        dq.addTail(2)
        dq.addTail(8)
        self.assertEqual(dq._min, 2)

        dq.removeTail()  # Removes 8
        self.assertEqual(dq._min, 2)

        dq.removeTail()  # Removes 2
        self.assertEqual(dq._min, 5)

        dq.removeTail()  # Removes 5
        self.assertIsNone(dq._min)

    def test_remove_min_last_instance(self):
        dq = MinDeque[int]()
        dq.addTail(4)
        dq.addTail(2)
        dq.addTail(2)
        dq.addTail(5)
        self.assertEqual(dq._min, 2)

        dq.removeFront()  # Removes 4
        self.assertEqual(dq._min, 2)

        dq.removeFront()  # Removes 2 (first instance)
        self.assertEqual(dq._min, 2)

        dq.removeFront()  # Removes 2 (last instance)
        self.assertEqual(dq._min, 5)

    def test_remove_until_empty(self):
        dq = MinDeque[int]()
        dq.addTail(10)
        dq.addTail(5)
        dq.addTail(7)
        self.assertEqual(dq._min, 5)

        dq.removeFront()
        dq.removeFront()
        dq.removeFront()
        self.assertIsNone(dq._min)


class TestBalancedBrackets(unittest.TestCase):
    def test_empty_string(self):
        self.assertTrue(is_balanced(""))

    def test_single_pair(self):
        self.assertTrue(is_balanced("()"))
        self.assertTrue(is_balanced("[]"))
        self.assertTrue(is_balanced("{}"))

    def test_multiple_pairs(self):
        self.assertTrue(is_balanced("()[]{}"))
        self.assertTrue(is_balanced("({[]})"))

    def test_unbalanced_missing_closing(self):
        self.assertFalse(is_balanced("("))
        self.assertFalse(is_balanced("({["))

    def test_unbalanced_wrong_order(self):
        self.assertFalse(is_balanced("([)]"))
        self.assertFalse(is_balanced("{(})"))

    def test_unbalanced_extra_closing(self):
        self.assertFalse(is_balanced("())"))
        self.assertFalse(is_balanced("()]"))

    def test_long_balanced(self):
        self.assertTrue(is_balanced("((({{{[[[]]]}}})))"))
        self.assertTrue(is_balanced("(){}[]({[]})"))

    def test_long_unbalanced(self):
        self.assertFalse(is_balanced("((({{{[[[}}})))"))
        self.assertFalse(is_balanced("(){}[({[})])"))


if __name__ == "__main__":
    unittest.main()
