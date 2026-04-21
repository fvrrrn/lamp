import unittest

from t04 import Stack
from t04_2 import AvgStack, Just, MinStack, Nothing, RPNEvaluator, check_brackets


class TestStack(unittest.TestCase):
    def test_base_append_and_del(self):
        s = Stack()
        s.push(1)
        expect_pop = s.pop()
        expect_pop_2 = s.pop()
        self.assertEqual(expect_pop, 1)
        self.assertIsNone(expect_pop_2)

    def test_base_size(self):
        s = Stack()
        self.assertEqual(s.size(), 0)
        s.push(1)
        s.push(1)
        s.push(1)
        s.push(1)
        self.assertEqual(s.size(), 4)
        s.pop()
        s.pop()
        s.pop()
        s.pop()
        self.assertEqual(s.size(), 0)

    def test_base_peek(self):
        s = Stack()
        s.push(96)
        s.push(97)
        s.push(98)
        s.push(99)
        self.assertEqual(s.peek(), 99)
        s.pop()
        self.assertEqual(s.peek(), 98)
        s.pop()
        self.assertEqual(s.peek(), 97)
        s.pop()
        self.assertEqual(s.peek(), 96)
        s.pop()
        self.assertIsNone(s.peek())
        s.pop()
        self.assertIsNone(s.peek())

    def test_base_pop(self):
        s = Stack()
        s.push(96)
        s.push(97)
        self.assertEqual(s.size(), 2)
        self.assertEqual(s.pop(), 97)
        self.assertEqual(s.pop(), 96)
        self.assertIsNone(s.pop())
        self.assertIsNone(s.pop())


class TestStack2(unittest.TestCase):
    def test_t4_5(self):
        self.assertTrue(check_brackets(""))

        self.assertFalse(check_brackets("("))
        self.assertFalse(check_brackets("{"))
        self.assertFalse(check_brackets("["))

        self.assertFalse(check_brackets(")"))
        self.assertFalse(check_brackets("}"))
        self.assertFalse(check_brackets("]"))

        self.assertFalse(check_brackets("(]"))
        self.assertFalse(check_brackets("{)"))
        self.assertFalse(check_brackets("[}"))
        self.assertFalse(check_brackets("({[})]"))

        self.assertTrue(check_brackets("()"))
        self.assertTrue(check_brackets("{}"))
        self.assertTrue(check_brackets("[]"))
        self.assertTrue(check_brackets("({[]})"))
        self.assertTrue(check_brackets("([{}])"))

        self.assertFalse(check_brackets("(()"))
        self.assertFalse(check_brackets("({[})"))
        self.assertFalse(check_brackets("([)]"))
        self.assertFalse(check_brackets("{[)]}"))

    def test_min_stack_operations(self):
        min_stack = MinStack()

        self.assertIsNone(min_stack.min())

        min_stack.push(3)
        min_stack.push(2)
        min_stack.push(5)

        self.assertEqual(min_stack.min(), 2)

        self.assertEqual(min_stack.pop(), 5)
        self.assertEqual(min_stack.min(), 2)

        self.assertEqual(min_stack.pop(), 2)
        self.assertEqual(min_stack.min(), 3)

        min_stack.push(1)
        self.assertEqual(min_stack.min(), 1)

        self.assertEqual(min_stack.pop(), 1)
        self.assertEqual(min_stack.min(), 3)

        min_stack.pop()
        self.assertIsNone(min_stack.min())

        min_stack.push(3)
        min_stack.push(3)
        min_stack.push(3)
        self.assertEqual(min_stack.min(), 3)

        self.assertEqual(min_stack.pop(), 3)
        self.assertEqual(min_stack.min(), 3)
        self.assertEqual(min_stack.pop(), 3)
        self.assertEqual(min_stack.min(), 3)

        min_stack.pop()
        self.assertIsNone(min_stack.min())

    def test_avg_stack_operations(self):
        avg_stack = AvgStack()

        self.assertEqual(avg_stack.avg(), 0)

        avg_stack.push(3)
        self.assertEqual(avg_stack.avg(), 3.0)
        avg_stack.push(2)
        self.assertEqual(avg_stack.avg(), 2.5)
        avg_stack.push(5)
        self.assertEqual(avg_stack.avg(), 3.3333333333333335)

        self.assertEqual(avg_stack.pop(), 5)
        self.assertEqual(avg_stack.avg(), 2.5)

        self.assertEqual(avg_stack.pop(), 2)
        self.assertEqual(avg_stack.avg(), 3.0)

        avg_stack.push(1)
        self.assertEqual(avg_stack.avg(), 2.0)

        self.assertEqual(avg_stack.pop(), 1)
        self.assertEqual(avg_stack.avg(), 3.0)

        avg_stack.pop()
        self.assertEqual(avg_stack.avg(), 0)

        avg_stack.push(3)
        avg_stack.push(3)
        avg_stack.push(3)
        self.assertEqual(avg_stack.avg(), 3.0)

    def test_rpn_operations(self):
        evaluator = RPNEvaluator()

        evaluator.append("12+")
        result = evaluator.operands.pop()
        match result:
            case Just(value):
                self.assertEqual(value, 3)
            case Nothing():
                self.fail("Result should not be Nothing.")

        evaluator.append("12-")
        result = evaluator.operands.pop()
        match result:
            case Just(value):
                self.assertEqual(value, -1)
            case Nothing():
                self.fail("Result should not be Nothing.")

        evaluator.append("22*")
        result = evaluator.operands.pop()
        match result:
            case Just(value):
                self.assertEqual(value, 4)
            case Nothing():
                self.assertEqual(result, Nothing())

        evaluator.append("42/")
        result = evaluator.operands.pop()
        match result:
            case Just(value):
                self.assertEqual(value, 2)
            case Nothing():
                self.fail("Result should not be Nothing.")

        evaluator.append("01/")
        result = evaluator.operands.pop()
        match result:
            case Just(value):
                self.assertEqual(value, 0)
            case Nothing():
                self.fail("Result should not be Nothing.")

        evaluator.append("00/")
        result = evaluator.operands.pop()
        match result:
            case Just(value):
                self.fail("Result should be Nothing due to division by zero.")
            case Nothing():
                self.assertEqual(result, Nothing())

        evaluator.append("82+5*9+")
        result = evaluator.append("=")
        match result:
            case Just(value):
                self.assertEqual(value, 59)
            case Nothing():
                self.fail("Result should not be Nothing.")


if __name__ == "__main__":
    unittest.main()
