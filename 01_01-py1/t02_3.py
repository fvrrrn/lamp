import unittest
from typing import cast

from t02 import LinkedList2 as LinkedList
from t02 import Node
from t02_2 import (
    DummyLinkedList,
    LoopLinkedList2,
    MergeableLinkedList2,
    ReversibleLinkedList2,
    SortableLinkedList2,
)


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
        values = list(ll)
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
        values = list(ll)
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
        print(ll)

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

        values = list(ll)
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


class TestLinkedList2Extensions(unittest.TestCase):
    def _values(self, ll: LinkedList) -> list:
        result = []
        node = ll.head
        while node is not None:
            result.append(node.value)
            node = node.next
        return result

    def test_reversed_empty(self):
        ll = ReversibleLinkedList2[int]()
        self.assertEqual(list(reversed(ll)), [])

    def test_reversed_single(self):
        ll = ReversibleLinkedList2[int]()
        ll.add_in_tail(Node(1))
        self.assertEqual(list(reversed(ll)), [1])

    def test_reversed_multiple(self):
        ll = ReversibleLinkedList2[int]()
        ll.add_in_tail(Node(1))
        ll.add_in_tail(Node(2))
        ll.add_in_tail(Node(3))
        self.assertEqual(list(reversed(ll)), [3, 2, 1])

    def test_has_loop_empty(self):
        ll = LoopLinkedList2[int]()
        self.assertFalse(ll.has_loop())

    def test_has_loop_false(self):
        ll = LoopLinkedList2[int]()
        ll.add_in_tail(Node(1))
        ll.add_in_tail(Node(2))
        ll.add_in_tail(Node(3))
        self.assertFalse(ll.has_loop())

    def test_has_loop_true(self):
        ll = LoopLinkedList2[int]()
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)
        ll.add_in_tail(node1)
        ll.add_in_tail(node2)
        ll.add_in_tail(node3)
        node3.next = node1
        self.assertTrue(ll.has_loop())

    def test_mutable_sort_empty(self):
        ll = SortableLinkedList2[int]()
        ll.mutable_sort()
        self.assertIsNone(ll.head)

    def test_mutable_sort_single(self):
        ll = SortableLinkedList2[int]()
        ll.add_in_tail(Node(5))
        ll.mutable_sort()
        self.assertEqual(self._values(ll), [5])

    def test_mutable_sort_basic(self):
        ll = SortableLinkedList2[int]()
        ll.add_in_tail(Node(3))
        ll.add_in_tail(Node(1))
        ll.add_in_tail(Node(2))
        ll.mutable_sort()
        self.assertEqual(self._values(ll), [1, 2, 3])

    def test_mutable_sort_reverse_order(self):
        ll = SortableLinkedList2[int]()
        ll.add_in_tail(Node(3))
        ll.add_in_tail(Node(2))
        ll.add_in_tail(Node(1))
        ll.mutable_sort()
        self.assertEqual(self._values(ll), [1, 2, 3])

    def test_mutable_sort_duplicates(self):
        ll = SortableLinkedList2[int]()
        ll.add_in_tail(Node(3))
        ll.add_in_tail(Node(1))
        ll.add_in_tail(Node(3))
        ll.add_in_tail(Node(1))
        ll.mutable_sort()
        self.assertEqual(self._values(ll), [1, 1, 3, 3])

    def test_mutable_sort_returns_self(self):
        ll = SortableLinkedList2[int]()
        ll.add_in_tail(Node(2))
        ll.add_in_tail(Node(1))
        self.assertIs(ll.mutable_sort(), ll)

    def test_mutable_sort_preserves_links(self):
        ll = SortableLinkedList2[int]()
        ll.add_in_tail(Node(3))
        ll.add_in_tail(Node(1))
        ll.add_in_tail(Node(2))
        ll.mutable_sort()
        node = ll.head
        while node is not None and node.next is not None:
            self.assertIs(node.next.prev, node)
            node = node.next

    def test_merge_basic(self):
        l1 = SortableLinkedList2[int]()
        l1.add_in_tail(Node(3))
        l1.add_in_tail(Node(1))
        l2 = SortableLinkedList2[int]()
        l2.add_in_tail(Node(4))
        l2.add_in_tail(Node(2))
        merged = MergeableLinkedList2.merge(l1, l2)
        self.assertEqual(self._values(merged), [1, 2, 3, 4])

    def test_merge_both_empty(self):
        l1: SortableLinkedList2[int] = SortableLinkedList2()
        l2: SortableLinkedList2[int] = SortableLinkedList2()
        merged = MergeableLinkedList2.merge(l1, l2)
        self.assertIsNone(merged.head)

    def test_merge_one_empty(self):
        l1 = SortableLinkedList2[int]()
        l1.add_in_tail(Node(1))
        l1.add_in_tail(Node(3))
        l2: SortableLinkedList2[int] = SortableLinkedList2()
        merged = MergeableLinkedList2.merge(l1, l2)
        self.assertEqual(self._values(merged), [1, 3])

    def test_merge_equal_elements(self):
        l1 = SortableLinkedList2[int]()
        l1.add_in_tail(Node(2))
        l1.add_in_tail(Node(2))
        l2 = SortableLinkedList2[int]()
        l2.add_in_tail(Node(2))
        l2.add_in_tail(Node(2))
        merged = MergeableLinkedList2.merge(l1, l2)
        self.assertEqual(self._values(merged), [2, 2, 2, 2])

    def test_merge_result_is_sorted(self):
        l1 = SortableLinkedList2[int]()
        l1.add_in_tail(Node(5))
        l1.add_in_tail(Node(2))
        l1.add_in_tail(Node(8))
        l2 = SortableLinkedList2[int]()
        l2.add_in_tail(Node(6))
        l2.add_in_tail(Node(1))
        l2.add_in_tail(Node(3))
        merged = MergeableLinkedList2.merge(l1, l2)
        values = self._values(merged)
        self.assertEqual(values, sorted(values))


class TestDummyLinkedList(unittest.TestCase):
    def _values(self, ll: DummyLinkedList) -> list:
        return [node.value for node in ll]

    def _rvalues(self, ll: DummyLinkedList) -> list:
        return [node.value for node in reversed(ll)]

    # -- init / head --

    def test_empty_list(self):
        ll: DummyLinkedList[int] = DummyLinkedList()
        self.assertEqual(len(ll), 0)
        self.assertIsNone(ll.head)

    def test_init_with_values(self):
        ll = DummyLinkedList[int](1, 2, 3)
        self.assertEqual(self._values(ll), [1, 2, 3])
        self.assertEqual(len(ll), 3)
        self.assertEqual(ll.head, 1)

    # -- append / prepend --

    def test_append_updates_head_on_first_insert(self):
        ll: DummyLinkedList[int] = DummyLinkedList()
        ll.append(42)
        self.assertEqual(ll.head, 42)
        self.assertEqual(len(ll), 1)

    def test_append_multiple(self):
        ll: DummyLinkedList[int] = DummyLinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        self.assertEqual(self._values(ll), [1, 2, 3])

    def test_prepend_becomes_new_head(self):
        ll = DummyLinkedList[int](2, 3)
        ll.prepend(1)
        self.assertEqual(self._values(ll), [1, 2, 3])
        self.assertEqual(ll.head, 1)

    def test_prepend_empty(self):
        ll: DummyLinkedList[int] = DummyLinkedList()
        ll.prepend(7)
        self.assertEqual(ll.head, 7)
        self.assertEqual(len(ll), 1)

    # -- iter / reversed --

    def test_iter_empty(self):
        ll: DummyLinkedList[int] = DummyLinkedList()
        self.assertEqual(self._values(ll), [])

    def test_reversed(self):
        ll = DummyLinkedList[int](1, 2, 3)
        self.assertEqual(self._rvalues(ll), [3, 2, 1])

    def test_forward_and_backward_agree(self):
        ll = DummyLinkedList[int](1, 2, 3, 4, 5)
        self.assertEqual(self._values(ll), list(reversed(self._rvalues(ll))))

    # -- find / find_all --

    def test_find_existing(self):
        ll = DummyLinkedList[int](1, 2, 3)
        node = ll.find(2)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 2)

    def test_find_missing(self):
        ll = DummyLinkedList[int](1, 2, 3)
        self.assertIsNone(ll.find(99))

    def test_find_all(self):
        ll = DummyLinkedList[int](1, 2, 1, 3, 1)
        nodes = ll.find_all(1)
        self.assertEqual(len(nodes), 3)
        self.assertTrue(all(n.value == 1 for n in nodes))

    # -- delete: all three positions use the same two-line rewire --

    def test_delete_middle(self):
        ll = DummyLinkedList[int](1, 2, 3)
        ll.delete(2)
        self.assertEqual(self._values(ll), [1, 3])
        self.assertEqual(len(ll), 2)

    def test_delete_head(self):
        ll = DummyLinkedList[int](1, 2, 3)
        ll.delete(1)
        self.assertEqual(self._values(ll), [2, 3])
        self.assertEqual(ll.head, 2)

    def test_delete_tail(self):
        ll = DummyLinkedList[int](1, 2, 3)
        ll.delete(3)
        self.assertEqual(self._values(ll), [1, 2])

    def test_delete_only_node(self):
        ll = DummyLinkedList[int](42)
        ll.delete(42)
        self.assertEqual(len(ll), 0)
        self.assertIsNone(ll.head)

    def test_delete_all(self):
        ll = DummyLinkedList[int](1, 2, 1, 2, 1)
        ll.delete(1, all=True)
        self.assertEqual(self._values(ll), [2, 2])

    def test_delete_preserves_links(self):
        ll = DummyLinkedList[int](1, 2, 3)
        ll.delete(2)
        self.assertEqual(self._values(ll), [1, 3])
        self.assertEqual(self._rvalues(ll), [3, 1])

    # -- clean --

    def test_clean(self):
        ll = DummyLinkedList[int](1, 2, 3)
        ll.clean()
        self.assertEqual(len(ll), 0)
        self.assertIsNone(ll.head)
        self.assertEqual(self._values(ll), [])

    def test_clean_then_append(self):
        ll = DummyLinkedList[int](1, 2, 3)
        ll.clean()
        ll.append(99)
        self.assertEqual(self._values(ll), [99])


if __name__ == "__main__":
    unittest.main()
