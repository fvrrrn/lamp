import unittest
from typing import cast

from t01 import LinkedList, Node


class TestLinkedList(unittest.TestCase):
    def test_add_in_tail(self):
        ll = LinkedList[int]()
        node1 = Node(1)
        node2 = Node(2)
        ll.add_in_tail(node1)
        ll.add_in_tail(node2)
        self.assertEqual(ll.head, node1)
        self.assertEqual(ll.tail, node2)
        # will not ever throw
        assert ll.head is not None
        self.assertEqual(ll.head.next, node2)

    def test_find(self):
        ll = LinkedList()
        node1 = Node(10)
        node2 = Node(20)
        ll.add_in_tail(node1)
        ll.add_in_tail(node2)
        found = ll.find(20)
        self.assertEqual(found, node2)

    def test_find_not_found(self):
        ll = LinkedList()
        ll.add_in_tail(Node(5))
        self.assertIsNone(ll.find(99))

    def test_len(self):
        ll = LinkedList()
        self.assertEqual(ll.len(), 0)
        ll.add_in_tail(Node(1))
        ll.add_in_tail(Node(2))
        self.assertEqual(ll.len(), 2)

    def test_clean(self):
        ll = LinkedList()
        ll.add_in_tail(Node(1))
        ll.add_in_tail(Node(2))
        ll.clean()
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(ll.len(), 0)

    def test_delete_only_node(self):
        ll = LinkedList[int]()
        node = Node(10)
        ll.add_in_tail(node)
        ll.delete(10)
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)

    def test_delete_tail_only(self):
        ll = LinkedList[int]()
        ll.add_in_tail(Node(1))
        node = Node(2)
        ll.add_in_tail(node)
        ll.delete(2)
        self.assertEqual(cast(Node[int], ll.tail).value, 1)
        self.assertIsNone(cast(Node[int], ll.tail).next)

    def test_delete_head_only(self):
        ll = LinkedList[int]()
        node1 = Node(1)
        ll.add_in_tail(node1)
        ll.add_in_tail(Node(2))
        ll.delete(1)
        self.assertEqual(cast(Node[int], ll.head).value, 2)
        self.assertIsNone(cast(Node[int], ll.head).prev)

    def test_delete_middle_node(self):
        ll = LinkedList[int]()
        ll.add_in_tail(Node(1))
        middle = Node(2)
        ll.add_in_tail(middle)
        ll.add_in_tail(Node(3))
        ll.delete(2)
        values = [node.value for node in ll]
        self.assertEqual(values, [1, 3])

    def test_delete_multiple_all_flag(self):
        ll = LinkedList[int]()
        ll.add_in_tail(Node(5))
        ll.add_in_tail(Node(5))
        ll.add_in_tail(Node(5))
        ll.delete(5, all=True)
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)

    def test_delete_multiple_all_flag_2(self):
        ll = LinkedList[int]()
        node1 = Node(1)
        ll.add_in_tail(node1)
        ll.add_in_tail(Node(5))
        ll.add_in_tail(Node(5))
        ll.add_in_tail(Node(5))
        ll.delete(5, all=True)
        self.assertEqual(ll.head, node1)
        self.assertEqual(ll.tail, node1)

    def test_delete_multiple_all_flag_3(self):
        ll = LinkedList[int]()
        node1 = Node(1)
        node2 = Node(2)
        ll.add_in_tail(node1)
        ll.add_in_tail(node2)
        ll.add_in_tail(Node(5))
        ll.add_in_tail(Node(5))
        ll.add_in_tail(Node(5))
        ll.delete(5, all=True)
        self.assertEqual(ll.head, node1)
        self.assertEqual(ll.tail, node2)

    def test_delete_first_occurrence_only(self):
        ll = LinkedList[int]()
        ll.add_in_tail(Node(1))
        ll.add_in_tail(Node(2))
        ll.add_in_tail(Node(2))
        ll.add_in_tail(Node(3))
        ll.delete(2)
        values = [node.value for node in ll]
        self.assertEqual(values, [1, 2, 3])

    def test_insert_into_empty_list(self):
        ll = LinkedList[int]()
        node = Node(1)
        ll.insert(None, node)
        self.assertEqual(ll.head, node)
        self.assertEqual(ll.tail, node)
        self.assertIsNone(node.prev)
        self.assertIsNone(node.next)

    def test_insert_when_after_is_none(self):
        ll = LinkedList[int]()
        node1 = Node(1)
        ll.add_in_tail(node1)
        node2 = Node(2)
        ll.insert(None, node2)
        self.assertEqual(ll.tail, node2)
        self.assertEqual(node2.prev, node1)
        self.assertEqual(node1.next, node2)
        self.assertEqual(ll.head, node1)
        self.assertIsNone(node2.next)
        self.assertEqual(ll.len(), 2)

    def test_insert_after_head(self):
        ll = LinkedList[int]()
        node1 = Node(1)
        node2 = Node(2)
        ll.add_in_tail(node1)
        ll.insert(node1, node2)
        self.assertEqual(node1.next, node2)
        self.assertEqual(node2.prev, node1)
        self.assertEqual(ll.tail, node2)
        self.assertEqual(ll.head, node1)

    def test_insert_in_middle(self):
        ll = LinkedList[int]()
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)
        ll.add_in_tail(node1)
        ll.add_in_tail(node3)
        ll.insert(node1, node2)
        self.assertEqual(node1.next, node2)
        self.assertEqual(node2.prev, node1)
        self.assertEqual(node2.next, node3)
        self.assertEqual(node3.prev, node2)

    def test_insert_after_tail(self):
        ll = LinkedList[int]()
        node1 = Node(1)
        ll.add_in_tail(node1)
        node2 = Node(2)
        ll.insert(node1, node2)
        self.assertEqual(ll.head, node1)
        self.assertEqual(ll.tail, node2)
        self.assertEqual(node1.next, node2)
        self.assertEqual(node2.prev, node1)
        self.assertIsNone(node2.next)

    def test_insert_middle(self):
        ll = LinkedList[str]()
        a1 = Node("a1")
        a2 = Node("a2")
        a3 = Node("a3")
        a4 = Node("a4")
        a5 = Node("a5")
        a7 = Node("a7")

        ll.add_in_tail(a1)
        ll.add_in_tail(a2)
        ll.add_in_tail(a3)
        ll.add_in_tail(a4)
        ll.add_in_tail(a5)

        ll.insert(a3, a7)

        values = [node.value for node in ll]
        self.assertEqual(values, ["a1", "a2", "a3", "a7", "a4", "a5"])

    def test_add_in_head_empty_list(self):
        ll = LinkedList[int]()
        node = Node(1)
        ll.add_in_head(node)
        self.assertIs(ll.head, node)
        self.assertIs(ll.tail, node)
        self.assertEqual(ll.size, 1)
        self.assertIsNone(node.prev)
        self.assertIsNone(node.next)

    def test_add_in_head_single_node_list(self):
        ll = LinkedList[int]()
        first = Node(1)
        ll.add_in_tail(first)

        second = Node(0)
        ll.add_in_head(second)

        self.assertIs(ll.head, second)
        self.assertIs(ll.tail, first)
        self.assertEqual(ll.size, 2)
        self.assertIs(second.next, first)
        self.assertIsNone(second.prev)
        self.assertIs(first.prev, second)
        self.assertIsNone(first.next)

    def test_add_in_head_multiple_nodes_list(self):
        ll = LinkedList[int]()
        first = Node(2)
        second = Node(3)
        ll.add_in_tail(first)
        ll.add_in_tail(second)

        new_head = Node(1)
        ll.add_in_head(new_head)

        self.assertIs(ll.head, new_head)
        self.assertEqual(ll.size, 3)
        self.assertIs(new_head.next, first)
        self.assertIsNone(new_head.prev)
        self.assertIs(first.prev, new_head)
        self.assertIs(first.next, second)
        self.assertIs(second.prev, first)
        self.assertIsNone(second.next)


if __name__ == "__main__":
    unittest.main()
