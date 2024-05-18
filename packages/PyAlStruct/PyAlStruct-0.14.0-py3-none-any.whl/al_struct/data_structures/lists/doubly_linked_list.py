from typing import Any

from al_struct.data_structures.lists.base_linked_list import BaseLinkedList
from al_struct.utils.exceptions import EmptyListException
from al_struct.utils.nodes import BinaryNode


class DoublyLinkedList(BaseLinkedList):
    """Doubly Linked List data structure."""

    def __init__(self):
        super().__init__()
        self._head: BinaryNode | None = None
        self._tail: BinaryNode | None = None

    def __str__(self):
        values = []
        temp: BinaryNode = self._head
        while temp:
            values.append(str(temp.data))
            temp = temp.next
        return " <-> ".join(values)

    def __repr__(self):
        return f"PyAlStruct.DoublyLinkedList({str(self)})"

    def is_empty(self) -> bool:
        """
        Check if the linked list is empty.
        :returns: bool -- True if the linked list is empty, otherwise False.
        """
        return self._head is None

    def prepend(self, data: Any) -> None:
        """
        Add a new node with data to the end of the list.
        :param data: The data to be added to the list.
        """
        node = BinaryNode(data, next_node=self._head)
        if self._head is not None:
            node.next = self._head
            self._head.prev = node
        self._head = node
        if self._head.next is None:
            self._tail = self._head
        self._size += 1

    def append(self, data: Any) -> None:
        """
        Add a new node with data to the end of the list.
        :param data: The data to be added to the list.
        """
        node = BinaryNode(data, prev_node=self._tail)
        if self._head is None:
            self._head = node
            self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def get_tail(self) -> Any:
        """
        Get data of the last node in the list.
        :return: The data of the last node in the list.
        """
        if self._tail is None:
            raise EmptyListException()
        return self._tail.data

    def reverse(self) -> None:
        """
        Reverse the order of the list.
        """
        if self._head is None:
            raise EmptyListException()
        current: BinaryNode = self._head
        next_node: BinaryNode = self._head.next
        current.next = None
        current.prev = next_node
        while next_node is not None:
            temp: BinaryNode = next_node.next
            next_node.next = current
            next_node.prev = temp
            current = next_node
            next_node = temp
        self._head = current

    def circular_permutation(self, amount: int) -> None:
        """
        Perform a circular permutation on the list with given amount.
        :param amount: The amount to perform the circular permutation.
        """
        for i in range(amount):
            self.append(self.delete(self.get_head()))
