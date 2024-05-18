from typing import Any

from al_struct.utils.exceptions import EmptyStackException
from al_struct.utils.nodes import Node


class Stack:
    """Simple stack data structure."""

    def __init__(self):
        self._top: Node | None = None
        self._size: int = 0

    def __str__(self):
        values = []
        temp: Node = self._top
        while temp:
            values.append(str(temp.data))
            temp = temp.next
        return ", ".join(values)

    def __repr__(self):
        return f"PyAlStruct.Stack({str(self)})"

    def __len__(self):
        return self._size

    def __iter__(self):
        self._current = self._top
        return self

    def __next__(self):
        if self._current:
            current = self._current
            self._current = self._current.next
            return current.data
        else:
            raise StopIteration

    @property
    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        """
        Check if the stack is empty.
        :returns: bool -- True if the stack is empty, otherwise False.
        """
        return self._top is None

    def push(self, item: Any) -> None:
        """
        Add a new item to the top of the stack.
        :param item: The item to be added to the stack.
        """
        node: Node = Node(item)
        node.next = self._top
        self._top = node
        self._size += 1

    def pop(self) -> None:
        """
        Removes and returns an item from the top of the stack.
        :return: The item at the top of the stack if exists.
        :raise EmptyStackException: If the stack is empty.
        """
        if self._top is None:
            raise EmptyStackException()
        item = self._top.data
        temp = self._top
        self._top = self._top.next
        del temp
        self._size -= 1
        return item

    def peek(self) -> Any:
        """
        Return the item in the top of the stack without removing it.
        :return: The item of the node at the top of the stack.
        """
        if not self._top:
            raise EmptyStackException()
        return self._top.data

    def reverse(self) -> None:
        """
        Reverse the order of the stack elements.
        """
        stack = Stack()
        while not self.is_empty():
            stack.push(self.pop())
        self._top = stack._top

    def circular_permutation(self, amount: int) -> None:
        """
        Perform a circular permutation on the stack with given amount.
        :param amount: The amount to perform the circular permutation.
        """
        temp1: Stack = Stack()
        temp2: Stack = Stack()
        for i in range(amount):
            temp1.push(self.pop())
        while not self.is_empty():
            temp2.push(self.pop())
        while not temp1.is_empty():
            self.push(temp1.pop())
        while not temp2.is_empty():
            self.push(temp2.pop())
