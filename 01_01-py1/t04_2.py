from dataclasses import dataclass
from typing import Literal, Protocol, TypeVar

from t04 import Stack

type Maybe[T] = Just[T] | Nothing


# from _typeshed import SupportsDunderLT -> ModuleNotFoundError: No module named '_typeshed'
class SupportsBool(Protocol):
    def __bool__(self) -> bool: ...


_T_contra = TypeVar("_T_contra", contravariant=True)


class SupportsDunderLT(Protocol[_T_contra]):
    def __lt__(self, other: _T_contra, /) -> SupportsBool: ...


@dataclass(frozen=True)
class Just[T]:
    value: T


@dataclass(frozen=True)
class Nothing:
    pass


# TASK: 1.4.5
# TITLE: Check if a bracket string is balanced using any bracket map
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(n) -- stack holds at most n/2 open brackets at once
# REFLECTION:
#     Stack remembers which open brackets we have seen but not closed yet.
#     When a closing bracket comes, the top of the stack must be the matching
#     opener -- if not, return False. At the end the stack must be empty,
#     meaning every opener was closed.
#     Takes mapped_brackets as argument so the same logic works for any set
#     of bracket pairs, not just the default three.
def is_balanced(brackets: str, mapped_brackets: dict[str, str]) -> bool:
    s = Stack[str]()
    for bracket in brackets:
        match mapped_brackets.get(bracket):
            case None:
                if mapped_brackets.get(s.pop() or "") != bracket:
                    return False
            case _:
                s.push(bracket)
    return len(s) == 0


# TASK: 1.4.6
# TITLE: Check all three standard bracket types
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(n)
# REFLECTION:
#     Calls is_balanced with the full bracket map so the caller does not
#     need to pass the map each time.
def check_brackets(brackets: str) -> bool:
    return is_balanced(brackets, {"(": ")", "{": "}", "[": "]"})


# TASK: 1.4.7
# TITLE: Stack that returns the current minimum in O(1)
# TIME COMPLEXITY: push O(1), pop O(1), min O(1)
# SPACE COMPLEXITY: O(n) -- second stack stores up to n values
# REFLECTION:
#     A second stack tracks only the minimums seen so far. On push, if the
#     new value is less than or equal to the current min, push it to the
#     min stack too. On pop, if the removed value equals the current min,
#     pop the min stack as well. So the top of the min stack is always the
#     current minimum with no scanning needed.
class MinStack[T: SupportsDunderLT](Stack[T]):
    def __init__(self) -> None:
        super().__init__()
        self._min_stack: Stack[T] = Stack()

    def push(self, value: T) -> None:
        super().push(value)
        current_min = self._min_stack.peek()
        if current_min is None or not (current_min < value):
            self._min_stack.push(value)

    def pop(self) -> T | None:
        value = super().pop()
        if value == self._min_stack.peek():
            self._min_stack.pop()
        return value

    def min(self) -> T | None:
        return self._min_stack.peek()


# TASK: 1.4.8
# TITLE: Stack that returns the running average in O(1)
# TIME COMPLEXITY: push O(1), pop O(1), avg O(1)
# SPACE COMPLEXITY: O(1) extra -- just one integer stored
# REFLECTION:
#     Keep a running sum: add on push, subtract on pop. Average is always
#     sum / count with no need to look at all items. Works correctly because
#     Stack already tracks the count via __len__.
class AvgStack(Stack[int]):
    def __init__(self) -> None:
        super().__init__()
        self._sum: int = 0

    def push(self, value: int) -> None:
        super().push(value)
        self._sum += value

    def pop(self) -> int | None:
        value = super().pop()
        if value is not None:
            self._sum -= value
        return value

    def avg(self) -> float:
        if len(self) == 0:
            return 0
        return self._sum / len(self)


# TASK: 1.4.9
# TITLE: Evaluate RPN expressions using two stacks
# TIME COMPLEXITY: O(n) -- one pass over the input string
# SPACE COMPLEXITY: O(n) -- both stacks together hold at most n entries
# REFLECTION:
#     Two stacks: one for operators, one for operands. After each character,
#     if we have at least one operator and two operands, we evaluate and push
#     the result back. "=" pops and returns the final result.
#     Maybe[int] on the operands stack represents division by zero as Nothing
#     rather than raising an exception, so the caller can handle it as a value.
#     Right now Stack.pop() and Stack.peek() return T | None where None means
#     "stack is empty". For Stack[Maybe[int]] this mixes two absence meanings:
#     None (stack empty) and Nothing (division by zero). If Stack were rewritten
#     so that pop/peek return Maybe[T] instead of T | None, the operands stack
#     would return Maybe[Maybe[int]] -- outer Nothing means stack empty, inner
#     Nothing means bad result -- with no None anywhere in the type.
class RPNEvaluator:
    def __init__(self):
        self.operators = Stack[Literal["+", "-", "*", "/", "="]]()
        self.operands = Stack[Maybe[int]]()

    def append(self, s: str) -> None | Maybe[int]:
        for c in s:
            match c:
                case "+" | "-" | "*" | "/" | "=":
                    self.operators.push(c)
                case _ if c.isdigit():
                    self.operands.push(Just(int(c)))

            match len(self.operators), len(self.operands):
                case 0, _:
                    pass
                case _, 0:
                    pass
                case _, 1:
                    pass
                case _, _:
                    maybe_b = self.operands.pop()
                    maybe_a = self.operands.pop()
                    operator = self.operators.pop()
                    match maybe_a, operator, maybe_b:
                        case Just(a), "+", Just(b):
                            self.operands.push(Just(a + b))
                        case Just(a), "-", Just(b):
                            self.operands.push(Just(a - b))
                        case Just(a), "*", Just(b):
                            self.operands.push(Just(a * b))
                        case Just(a), "/", Just(b):
                            match b:
                                case 0:
                                    self.operands.push(Nothing())
                                case _:
                                    # although technically it is possible
                                    # to store floating-point numbers
                                    # I decided not to by strictly using integers
                                    self.operands.push(Just(a // b))
                        case _, "=", _:
                            return self.operands.pop()
