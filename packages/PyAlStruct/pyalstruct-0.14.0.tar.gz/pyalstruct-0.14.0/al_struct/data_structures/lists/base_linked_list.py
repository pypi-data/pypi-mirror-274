from typing import Any

from al_struct.utils.exceptions import EmptyListException, NodeNotFoundException
from al_struct.utils.nodes import Node, BinaryNode


class BaseLinkedList:
    """Base linked list data structure."""

    def __init__(self):
        self._head: Node | None = None
        self._size: int = 0

    def __len__(self):
        return self._size

    def __iter__(self):
        self._current = self._head
        return self

    def __next__(self):
        if self._current:
            current: Node = self._current
            self._current = self._current.next
            return current.data
        else:
            raise StopIteration

    @property
    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        """
        Check if the linked list is empty.
        :returns: bool -- True if the linked list is empty, otherwise False.
        """
        return self._head is None

    def get_head(self) -> Any:
        """
        Get data of the first node in the list.
        :return: The data of the first node in the list.
        """
        if self._head is None:
            raise EmptyListException()
        return self._head.data

    def get(self, data: Any) -> Any:
        """
        Return the node that contains data if exist in the list.
        :param data: The data to search for.
        :return: Node -- The node that contains data if exists.
        """
        temp: Node | BinaryNode = self._head
        while temp is not None:
            if temp.data == data:
                return temp
            temp = temp.next
        raise NodeNotFoundException(data)

    def get_all(self, data: Any) -> list[Any]:
        """
        Return a list of all the nodes data that contain data if exist in the list.
        :param data: The data to search for.
        :return: list[Any] -- List of all the nodes data that contain data in the list.
        """
        nodes: list[Any] = []
        temp: Node | BinaryNode = self._head
        while temp is not None:
            if temp.data == data:
                nodes.append(temp.data)
            temp = temp.next
        return nodes

    def search(self, data: Any) -> bool:
        """
        Return boolean value if data exists in the list.
        :param data: The data to search for.
        :return: bool -- True if data exists, otherwise False.
        :raises NodeNotFoundException: If the data is not found in the list.
        """
        temp: Node | BinaryNode = self._head
        while temp:
            if temp.data == data:
                return True
            temp = temp.next
        return False

    def index(self, data: Any) -> int:
        """
        Find the index of the first occurrence of data in the list.
        :param data: The data to search for in the list.
        :returns: int -- The index of the first occurrence of the data in the list.
        :raises NodeNotFoundException: If the data is not found in the list.
        """
        index: int = 0
        temp: Node | BinaryNode = self._head
        while temp is not None:
            if temp.data == data:
                return index
            temp = temp.next
            index += 1
        raise NodeNotFoundException(data)

    def indexes(self, data: Any) -> list[int]:
        """
        Find the indexes of the all occurrences of data in the list.
        :param data: The data to search for in the list.
        :return: list[int] -- List of indexes of all occurrences of the data in the list.
        """
        indexes: list[int] = []
        index: int = 0
        temp: Node | BinaryNode = self._head
        while temp is not None:
            if temp.data == data:
                indexes.append(index)
            temp = temp.next
            index += 1
        return indexes

    def _delete_node(self, target: Node | BinaryNode, head: Node | BinaryNode | None = None) -> Any:
        """Helper function to delete a node from the linked list."""
        value: Any = target.data
        if target is self._head:
            self._head = self._head.next
        else:
            head.next = target.next
        if type(target.next) is BinaryNode:
            target.next.prev = head
        del target
        self._size -= 1
        return value

    def delete(self, data: Any) -> Any:
        """
        Delete the first occurrence of data in the list.
        :param data: The data to be deleted
        :return: Any -- The data from the node that was deleted.
        """
        if self._head is None:
            raise EmptyListException()
        if self._head.data == data:
            return self._delete_node(self._head)
        current: Node | BinaryNode = self._head
        next_node: Node | BinaryNode = current.next
        while next_node is not None:
            if next_node.data == data:
                return self._delete_node(next_node, current)
            current = current.next
            next_node = current.next
        raise NodeNotFoundException(data)

    def delete_at_position(self, position: int) -> Any:
        """
        Delete  data at specific position from the list.\n
        0 means first node.\n
        -1 means last node.
        :param position: The position to delete.
        :return: The data from the node that was deleted.
        """
        if position > self._size - 1 or position < -self._size:
            raise IndexError(f"Position {position} is out of bounds")
        if position == 0:
            return self._delete_node(self._head)
        if position > 0:
            count: int = 0
            current: Node | BinaryNode = self._head
            temp: Node | BinaryNode = self._head
            while count < position:
                current = temp
                temp = temp.next
                count += 1
            return self._delete_node(temp, current)
        if position < 0:
            count: int = self._size
            current: Node | BinaryNode = self._head
            temp: Node | BinaryNode = self._head
            while count > -position:
                current = temp
                temp = temp.next
                count -= 1
            return self._delete_node(temp, current)

    def delete_all(self, data: Any) -> int:
        """
        Delete all occurrences of data in the list.
        :param data: The data to be deleted
        :return: int -- The count of removed occurrences from the data in the list.
        """
        count: int = 0
        if self._head is None:
            raise EmptyListException()
        while self._head.data == data:
            self._delete_node(self._head)
            count += 1
        current: Node | BinaryNode = self._head
        next_node: Node | BinaryNode = current.next
        while next_node is not None:
            while next_node.data == data:
                self._delete_node(next_node, current)
                next_node = current.next
                count += 1
            current = current.next
            next_node = current.next
        if count == 0:
            raise NodeNotFoundException(data)
        return count
