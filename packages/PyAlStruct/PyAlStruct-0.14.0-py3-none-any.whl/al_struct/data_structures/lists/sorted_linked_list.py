from typing import Any

from al_struct.data_structures.lists.base_linked_list import BaseLinkedList
from al_struct.utils.exceptions import EmptyListException
from al_struct.utils.nodes import Node


class SortedLinkedList(BaseLinkedList):

    def __init__(self):
        super().__init__()

    def __str__(self):
        values = []
        temp: Node = self._head
        while temp:
            values.append(str(temp.data))
            temp = temp.next
        del temp
        return " -> ".join(values)

    def __repr__(self):
        return f"PyAlStruct.SortedLinkedList({str(self)})"

    def append(self, data: Any) -> None:
        """
        Add a new node with data to the list, it will be sorted automatically.
        :param data: The data to be added to the list.
        """
        node: Node = Node(data)
        if self._head is None:
            self._head = node
            self._size += 1
            return
        if data < self._head.data or data == self._head.data:
            node.next = self._head
            self._head = node
            self._size += 1
            return
        temp: Node = self._head
        current: Node | None = None
        while temp.next and data > temp.data:
            current = temp
            temp = temp.next
        if data <= temp.data:
            current.next = node
            node.next = temp
            self._size += 1
            return
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
