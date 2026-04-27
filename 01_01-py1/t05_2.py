import ctypes

from t04 import Stack
from t05 import Queue


# TASK: 1.5.3
# TITLE: Rotate a queue by N positions
# TIME COMPLEXITY: O(n) -- at most size-1 dequeue/enqueue pairs
# SPACE COMPLEXITY: O(1) -- no extra storage
# REFLECTION:
#     Move the first N elements to the back one by one. Taking N modulo size
#     avoids doing a full rotation that would leave the queue unchanged, and
#     handles the case where N > size without extra branches.
def rotate_queue(queue: Queue, n: int):
    n = n % queue.size() if queue.size() > 0 else 0
    for _ in range(n):
        queue.enqueue(queue.dequeue())


# TASK: 1.5.4
# TITLE: Queue implemented with two stacks (with persistent dequeue history)
# TIME COMPLEXITY: enqueue O(1), dequeue O(1)
# SPACE COMPLEXITY: O(n) -- both stacks together hold all items ever enqueued
# REFLECTION:
#     One stack holds the currently queued items; the other accumulates every
#     item that was ever dequeued. This preserves a full audit trail: the
#     queued property merges both stacks to show the complete timeline.
#     Because items are pushed to and popped from the same stack, the order is
#     LIFO, making this more of a persistent stack than a classic FIFO queue --
#     but the two-stack structure cleanly separates live items from history.
class PersistentQueue:
    def __init__(self):
        self._enqueued = Stack()
        self._dequeued = Stack()

    @property
    def queued(self):
        for item in self._enqueued:
            yield item
        for item in reversed(self._dequeued):
            yield item

    @property
    def dequeued(self):
        return reversed(self._dequeued)

    @property
    def enqueued(self):
        return self._enqueued

    def __len__(self):
        return len(self._enqueued)

    def enqueue(self, value):
        self._enqueued.push(value)

    def dequeue(self):
        match self._enqueued.pop():
            case None:
                return None
            case value:
                self._dequeued.push(value)
                return value


# TASK: 1.5.5a
# TITLE: Reverse a queue into a new queue
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(n) -- a second queue holds all n items
# REFLECTION:
#     reversed() walks the doubly-linked list from tail to head via __reversed__,
#     so we get items in reverse order without any extra stack or index math.
#     The result is a fresh queue; the original is left untouched.
def reverse_queue(queue: Queue):
    reversed_queue = Queue()
    for value in reversed(queue):
        reversed_queue.enqueue(value)
    return reversed_queue


# TASK: 1.5.6
# TITLE: Circular queue backed by a fixed-size static array
# TIME COMPLEXITY: enqueue O(1), dequeue O(1), is_full O(1), is_empty O(1)
# SPACE COMPLEXITY: O(capacity) -- array allocated once at construction
# REFLECTION:
#     Two indices, _start and _end, advance with modulo arithmetic so they wrap
#     around the array instead of shifting data. _size tracks the count
#     separately so is_full and is_empty never need to compare pointer positions,
#     which avoids the classic off-by-one ambiguity between a full and an empty
#     circular buffer (both would have _start == _end without the size field).
class StaticQueue:
    def __init__(self, capacity):
        self._capacity = capacity
        self._queue = (capacity * ctypes.py_object)()
        self._start = 0
        self._end = 0
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._capacity

    def enqueue(self, item):
        if self.is_full():
            return None
        else:
            at = self._end
            self._queue[self._end] = item
            self._end = (self._end + 1) % self._capacity
            self._size += 1
            return at

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            item = self._queue[self._start]
            self._start = (self._start + 1) % self._capacity
            self._size -= 1
            return item

    def __getitem__(self, index: int):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        return self._queue[(self._start + index) % self._capacity]

    def __setitem__(self, index: int, value):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        self._queue[(self._start + index) % self._capacity] = value


# TASK: 1.5.5b
# TITLE: Reverse a StaticQueue in place using index swapping
# TIME COMPLEXITY: O(n) -- single pass over half the elements, each swap O(1)
# SPACE COMPLEXITY: O(1) -- no extra storage
# REFLECTION:
#     Because StaticQueue is backed by a ctypes array, indexed access is O(1),
#     so the standard two-pointer swap reversal runs in O(n) with no auxiliary
#     data structure needed.
def reverse_queue_in_place(static_queue: StaticQueue):
    n = static_queue._size
    for i in range(n // 2):
        static_queue[i], static_queue[n - 1 - i] = static_queue[n - 1 - i], static_queue[i]
