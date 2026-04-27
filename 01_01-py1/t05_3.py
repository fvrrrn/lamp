import random
import unittest

from t05 import Node, Queue
from t05_2 import (
    PersistentQueue,
    StaticQueue,
    reverse_queue,
    reverse_queue_in_place,
    rotate_queue,
)


class TestQueue(unittest.TestCase):
    def test_enqueue_single_item(self):
        queue = Queue[int]()
        queue.enqueue(10)
        self.assertEqual(len(queue), 1)
        assert isinstance(queue._head.next, Node)
        self.assertEqual(queue._head.next.value, 10)
        assert isinstance(queue._tail.prev, Node)
        self.assertEqual(queue._tail.prev.value, 10)

    def test_enqueue_multiple_items(self):
        queue = Queue[int]()
        queue.enqueue(10)
        queue.enqueue(20)
        queue.enqueue(30)

        self.assertEqual(len(queue), 3)
        assert isinstance(queue._head.next, Node)
        self.assertEqual(queue._head.next.value, 10)
        assert isinstance(queue._tail.prev, Node)
        self.assertEqual(queue._tail.prev.value, 30)
        assert isinstance(queue._head.next.next, Node)
        self.assertEqual(queue._head.next.next.value, 20)

    def test_dequeue_single_item(self):
        queue = Queue[int](10)
        value = queue.dequeue()

        self.assertEqual(value, 10)
        self.assertEqual(len(queue), 0)

    def test_dequeue_multiple_items(self):
        queue = Queue[int]()
        queue.enqueue(10)
        queue.enqueue(20)
        queue.enqueue(30)

        self.assertEqual(len(queue), 3)
        self.assertEqual(queue.dequeue(), 10)
        self.assertEqual(len(queue), 2)
        self.assertEqual(queue.dequeue(), 20)
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue.dequeue(), 30)
        self.assertEqual(len(queue), 0)

    def test_dequeue_empty_queue(self):
        queue = Queue[int]()
        value = queue.dequeue()

        self.assertIsNone(value)
        self.assertEqual(len(queue), 0)

    def test_size(self):
        queue = Queue[int](10, 20)
        self.assertEqual(queue.size(), 2)
        queue.enqueue(30)
        self.assertEqual(queue.size(), 3)
        queue.dequeue()
        self.assertEqual(queue.size(), 2)

    def test_str_representation(self):
        queue = Queue[int](10, 20, 30)
        self.assertEqual(str(queue), "10 -> 20 -> 30")

    def test_reversed(self):
        queue = Queue[int](10, 20, 30)
        reversed_values = list(reversed(queue))
        self.assertEqual([value for value in reversed_values], [30, 20, 10])


class TestQueueOneItem(unittest.TestCase):
    def setUp(self):
        self.s_queue = Queue()
        self.number = random.randint(0, 100)
        self.s_queue.enqueue(self.number)

    def test_one_item_size(self):
        self.assertEqual(self.s_queue.size(), 1)

    def test_one_item_enqueue(self):
        len_queue = self.s_queue.size()
        new_item = random.randint(0, 100)
        self.s_queue.enqueue(new_item)
        self.assertEqual(self.s_queue.size(), len_queue + 1)
        # self.assertEqual(self.s_queue.queue[-1], new_item)

    def test_one_item_dequeue(self):
        len_queue = self.s_queue.size()
        dequeue_result = self.s_queue.dequeue()
        self.assertEqual(dequeue_result, self.number)
        self.assertEqual(self.s_queue.size(), len_queue - 1)
        # self.assertEqual(self.s_queue.queue, [])


class TestQueueEmpty(unittest.TestCase):
    def setUp(self):
        self.s_queue = Queue()

    def test_empty_size(self):
        self.assertEqual(self.s_queue.size(), 0)

    def test_empty_enqueue(self):
        len_queue = self.s_queue.size()
        new_item = random.randint(0, 100)
        self.s_queue.enqueue(new_item)
        self.assertEqual(self.s_queue.size(), len_queue + 1)
        # self.assertEqual(self.s_queue.queue[-1], new_item)

    def test_empty_dequeue(self):
        len_queue = self.s_queue.size()
        dequeue_result = self.s_queue.dequeue()
        self.assertIsNone(dequeue_result)
        self.assertEqual(self.s_queue.size(), len_queue)
        # self.assertEqual(self.s_queue.queue, [])


class TestQueueManyItems(unittest.TestCase):
    def setUp(self):
        self.s_queue = Queue()
        number = random.randrange(3, 100)
        self.items_list = [random.randint(0, 100) for _ in range(number)]
        for item in self.items_list:
            self.s_queue.enqueue(item)

    def test_many_items_size(self):
        self.assertEqual(self.s_queue.size(), len(self.items_list))

    def test_many_items_enqueue(self):
        len_queue = self.s_queue.size()
        new_item = random.randint(0, 100)
        self.s_queue.enqueue(new_item)
        self.assertEqual(self.s_queue.size(), len_queue + 1)
        # self.assertEqual(self.s_queue.queue[-1], new_item)

    def test_many_items_dequeue(self):
        len_queue = self.s_queue.size()
        dequeue_result = self.s_queue.dequeue()
        self.assertEqual(dequeue_result, self.items_list[0])
        self.assertEqual(self.s_queue.size(), len_queue - 1)
        # self.assertListEqual(self.s_queue.queue, self.items_list[1:])


class TestRotateReverseAndCircularQueue(unittest.TestCase):
    def test_rotate_queue(self):
        queue = Queue()
        for i in range(1, 6):
            queue.enqueue(i)

        rotate_queue(queue, 0)
        self.assertListEqual(list(queue), [1, 2, 3, 4, 5])

        rotate_queue(queue, 2)
        self.assertListEqual(list(queue), [3, 4, 5, 1, 2])

        rotate_queue(queue, 5)
        self.assertListEqual(list(queue), [3, 4, 5, 1, 2])

        rotate_queue(queue, 7)
        self.assertListEqual(list(queue), [5, 1, 2, 3, 4])

        empty_queue = Queue()
        rotate_queue(empty_queue, 3)
        self.assertListEqual(list(empty_queue), [])

    def test_persistent_queue(self):
        q = PersistentQueue()

        self.assertEqual(len(q), 0)
        self.assertListEqual(list(q.enqueued), [])
        self.assertListEqual(list(q.dequeued), [])
        self.assertListEqual(list(q.queued), [])

        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)

        self.assertEqual(len(q), 3)
        self.assertListEqual(list(q.enqueued), [3, 2, 1])
        self.assertListEqual(list(q.dequeued), [])
        self.assertListEqual(list(q.queued), [3, 2, 1])

        self.assertEqual(q.dequeue(), 3)
        self.assertEqual(len(q), 2)
        self.assertListEqual(list(q.enqueued), [2, 1])
        self.assertListEqual(list(q.dequeued), [3])
        self.assertListEqual(list(q.queued), [2, 1, 3])

        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 1)
        self.assertIsNone(q.dequeue())

        self.assertEqual(len(q), 0)
        self.assertListEqual(list(q.enqueued), [])
        self.assertListEqual(list(q.dequeued), [3, 2, 1])
        self.assertListEqual(list(q.queued), [3, 2, 1])
        q.enqueue(5)
        self.assertListEqual(list(q.queued), [5, 3, 2, 1])
        self.assertListEqual(list(q.enqueued), [5])

    def test_reverse_queue(self):
        queue = Queue()
        for i in range(1, 6):
            queue.enqueue(i)

        reversed_queue = reverse_queue(queue)
        self.assertListEqual(list(reversed_queue), [5, 4, 3, 2, 1])

        empty_queue = Queue()
        reversed_empty = reverse_queue(empty_queue)
        self.assertListEqual(list(reversed_empty), [])

        single_element_queue = Queue()
        single_element_queue.enqueue(42)
        reversed_single = reverse_queue(single_element_queue)
        self.assertListEqual(list(reversed_single), [42])

    def test_reverse_queue_in_place(self):
        sq = StaticQueue(5)
        for i in range(1, 6):
            sq.enqueue(i)
        reverse_queue_in_place(sq)
        self.assertListEqual([sq[i] for i in range(sq._size)], [5, 4, 3, 2, 1])

        sq2 = StaticQueue(6)
        for i in range(1, 7):
            sq2.enqueue(i)
        reverse_queue_in_place(sq2)
        self.assertListEqual([sq2[i] for i in range(sq2._size)], [6, 5, 4, 3, 2, 1])

        empty_sq = StaticQueue(4)
        reverse_queue_in_place(empty_sq)
        self.assertListEqual([empty_sq[i] for i in range(empty_sq._size)], [])

        single_sq = StaticQueue(1)
        single_sq.enqueue(42)
        reverse_queue_in_place(single_sq)
        self.assertListEqual([single_sq[i] for i in range(single_sq._size)], [42])

    def test_static_queue(self):
        queue = StaticQueue(3)
        self.assertTrue(queue.is_empty())
        self.assertFalse(queue.is_full())

        self.assertEqual(queue.enqueue(10), 0)
        self.assertEqual(queue._queue[0], 10)
        self.assertEqual(queue._size, 1)

        self.assertEqual(queue.enqueue(20), 1)
        self.assertEqual(queue.enqueue(30), 2)
        self.assertTrue(queue.is_full())
        self.assertEqual(queue._size, 3)
        self.assertIsNone(queue.enqueue(40))

        self.assertEqual(queue.dequeue(), 10)
        self.assertEqual(queue.dequeue(), 20)
        self.assertEqual(queue.dequeue(), 30)
        self.assertTrue(queue.is_empty())
        self.assertIsNone(queue.dequeue())

        queue.enqueue(1)
        queue.enqueue(2)
        self.assertFalse(queue.is_empty())
        self.assertFalse(queue.is_full())
        self.assertEqual(queue.dequeue(), 1)
        queue.enqueue(3)
        self.assertEqual(queue.dequeue(), 2)
        self.assertEqual(queue.dequeue(), 3)
        self.assertTrue(queue.is_empty())

        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        self.assertTrue(queue.is_full())
        self.assertIsNone(queue.enqueue(4))
        self.assertEqual(queue.dequeue(), 1)
        queue.enqueue(4)
        self.assertEqual(queue.dequeue(), 2)
        self.assertEqual(queue.dequeue(), 3)
        self.assertEqual(queue.dequeue(), 4)
        self.assertTrue(queue.is_empty())


if __name__ == "__main__":
    unittest.main()
