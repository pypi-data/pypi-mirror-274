from typing import Any

from al_struct.data_structures.stacks import Stack
from al_struct.utils.exceptions import EmptyQueueException
from al_struct.utils.nodes import Node


class Queue:
    """Simple queue data structure."""

    def __init__(self):
        self._front: Node | None = None
        self._back: Node | None = None
        self._size: int = 0

    def __str__(self):
        values = []
        temp: Node = self._front
        while temp:
            values.append(str(temp.data))
            temp = temp.next
        return " | ".join(values)

    def __repr__(self):
        return f"PyAlStruct.Queue({str(self)})"

    def __len__(self):
        return self._size

    def __iter__(self):
        self._current = self._front
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
        Check if the queue is empty.
        :returns: bool -- True if the queue is empty, otherwise False.
        """
        return self._front is None

    def enqueue(self, item: Any) -> None:
        """
        Add a new node with item to the back of the queue.
        :param item: The item to be added to the queue.
        """
        node: Node = Node(item)
        if self._front is None:
            self._front = node
            self._back = node
            return
        self._back.next = node
        self._back = node

    def dequeue(self) -> None:
        """
        Removes and returns an item from the front of the queue.
        :return: The item at the front of the queue if exists.
        :raise EmptyQueueException: If the stack is empty.
        """
        if self._front is None:
            raise EmptyQueueException()
        if self._front == self._back:
            self._front = None
        data: Any = self._front.data
        temp: Node = self._front
        self._front = self._front.next
        del temp
        return data

    def reverse(self) -> None:
        """
        Reverse the order of the queue.
        """
        stack = Stack()
        while self.is_empty():
            stack.push(self.dequeue())
        while not stack.is_empty():
            self.enqueue(stack.pop())

    def circular_permutation(self, amount: int) -> None:
        """
        Perform a circular permutation on the queue with given amount.
        :param amount: The amount to perform the circular permutation.
        """
        for i in range(amount):
            self.enqueue(self.dequeue())
