from typing import Any

from al_struct.data_structures.lists.base_linked_list import BaseLinkedList
from al_struct.utils.exceptions import EmptyListException
from al_struct.utils.nodes import Node


class SinglyLinkedList(BaseLinkedList):
    """Singly linked list data structure."""

    def __init__(self):
        super().__init__()

    def __str__(self):
        values = []
        temp: Node = self._head
        while temp:
            values.append(str(temp.data))
            temp = temp.next
        return " -> ".join(values)

    def __repr__(self):
        return f"PyAlStruct.SinglyLinkedList({str(self)})"

    def prepend(self, data: Any) -> None:
        """
        Add a new node with data to the beginning of the list.
        :param data: The data to be added to the list.
        """
        node: Node = Node(data)
        if self._head is not None:
            node.next = self._head
        self._head = node
        self._size += 1

    def append(self, data: Any) -> None:
        """
        Add a new node with data to the end of the list.
        :param data: The data to be added to the list.
        """
        node: Node = Node(data)
        if not self._head:
            self._head = node
            self._size += 1
            return
        temp = self._head
        while temp.next:
            temp = temp.next
        temp.next = node
        self._size += 1

    def get_tail(self) -> Any:
        """
        Get data of the last node in the list.
        :return: The data of the last node in the list.
        """
        if not self._head:
            raise EmptyListException()
        temp: Node = self._head
        while temp.next:
            temp = temp.next
        return temp.data

    def reverse(self) -> None:
        """
        Reverse the order of the list.
        """
        if self._head is None:
            raise EmptyListException()
        previous: Node | None = None
        current: Node = self._head
        while current is not None:
            temp: Node = current.next
            current.next = previous
            previous = current
            current = temp
        self._head = previous

    def circular_permutation(self, amount: int) -> None:
        """
        Perform a circular permutation on the list with given amount.
        :param amount: The amount to perform the circular permutation.
        """
        for i in range(amount):
            self.append(self.delete(self.get_head()))
