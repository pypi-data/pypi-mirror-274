from typing import Any


class Node:
    """Basic node for linked data structures."""

    def __init__(self, data: Any = None, next_node: 'Node' = None):
        """
        Initialize a new node.
        :param data: The data to be stored in the node.
        :param next_node: The next node in the linked structure.
        """
        self._data: Any = data
        self._next: Node = next_node

    def __eq__(self, other: 'Node'):
        if isinstance(other, Node):
            return self.data == other.data and self.next == other.next
        return False

    @property
    def data(self) -> Any:
        return self._data

    @data.setter
    def data(self, data: Any) -> None:
        self._data = data

    @property
    def next(self) -> 'Node':
        return self._next

    @next.setter
    def next(self, ptr: 'Node') -> None:
        if not isinstance(ptr, (Node, type(None))):
            raise TypeError("The pointer should be a Node or None")
        self._next = ptr


class BinaryNode:
    """Node for double side linked data structures"""
    def __init__(self, data: Any = None, prev_node: 'BinaryNode' = None, next_node: 'BinaryNode' = None):
        """
        Initialize a new binary node.
        :param data: The data to be stored in the node.
        :param prev_node: The previous node
        :param next_node: The next node
        """
        self._data: Any = data
        self._prev: 'BinaryNode' = prev_node
        self._next: 'BinaryNode' = next_node

    def __eq__(self, other: 'BinaryNode'):
        if isinstance(other, BinaryNode):
            return self.data == other.data and self.prev == other.prev and self.next == other.next
        return False

    @property
    def data(self) -> Any:
        return self._data

    @data.setter
    def data(self, data: Any) -> None:
        self._data = data

    @property
    def prev(self) -> 'BinaryNode':
        return self._prev

    @prev.setter
    def prev(self, ptr: 'BinaryNode') -> None:
        if not isinstance(ptr, (BinaryNode, type(None))):
            raise TypeError("The pointer should be a BinaryNode or None")
        self._prev = ptr

    @property
    def next(self) -> 'BinaryNode':
        return self._next

    @next.setter
    def next(self, ptr: 'BinaryNode') -> None:
        if not isinstance(ptr, (BinaryNode, type(None))):
            raise TypeError("The pointer should be a BinaryNode or None")
        self._next = ptr


class TreeNode:
    """Node for binary tree based linked data structures"""

    def __init__(self, key: Any = None, left_node: 'TreeNode' = None, right_node: 'TreeNode' = None):
        """
        Initialize a new tree node.
        :param key: The data to be stored in the node.
        :param left_node: The previous node
        :param right_node: The next node
        """
        self._key: Any = key
        self._left: 'TreeNode' = left_node
        self._right: 'TreeNode' = right_node

    def __eq__(self, other: 'TreeNode'):
        if isinstance(other, TreeNode):
            return self.key == other.key and self.left == other.left and self.right == other.right
        return False

    @property
    def key(self) -> Any:
        return self._key

    @key.setter
    def key(self, data: Any) -> None:
        self._key = data

    @property
    def left(self) -> 'TreeNode':
        return self._left

    @left.setter
    def left(self, ptr: 'TreeNode') -> None:
        if not isinstance(ptr, (TreeNode, type(None))):
            raise TypeError("The pointer should be a TreeNode or None")
        self._left = ptr

    @property
    def right(self) -> 'TreeNode':
        return self._right

    @right.setter
    def right(self, ptr: 'TreeNode') -> None:
        if not isinstance(ptr, (TreeNode, type(None))):
            raise TypeError("The pointer should be a TreeNode or None")
        self._right = ptr
