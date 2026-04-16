from t01 import LinkedList, Node


# TASK: 1.1.8
# TITLE: Merge two equal-length linked lists by element-wise sum
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(n) -- new list of n nodes
# REFLECTION:
#     TLDR: the runtime len check is the right tool here, strict=False
#     signals to the reader that the invariant is already established externally.
#   - strict=False: zip already stops at the shorter iterable; by the time we
#     reach it the len check above has proved equality, so strict=True would be
#     a redundant second guard on a property we already own.
#   - Dependent types: Python has no native dependent types, so "LinkedList of
#     length N" cannot be expressed in the type signature, the length lives
#     only in the value, not the type. The closest approximations are:
#       * TypeVarTuple / Unpack for fixed-arity tuples (not applicable here,
#         length is dynamic and unknown at definition time)
#       * A phantom-type newtype like SameLengthPair[T] that enforces the
#         invariant at construction and erases it at use, possible but adds
#         complexity the caller must absorb, with no practical benefit in this
#         context.
# CODE:
def t1_8(l1: LinkedList[int], l2: LinkedList[int]) -> LinkedList[int] | None:
    if len(l1) != len(l2):
        return None
    merged = LinkedList[int]()
    for n1, n2 in zip(l1, l2, strict=False):
        merged.add_in_tail(Node(n1.value + n2.value))
    return merged
