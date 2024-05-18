from typing import Any

from al_struct.utils.exceptions import EmptyTreeException, NodeNotFoundException
from al_struct.utils.nodes import TreeNode


class BinarySearchTree:
    """Binary search tree data structure."""
    def __init__(self):
        self._root: TreeNode | None = None
        self._number_of_nodes: int = 0

    def __str__(self):
        return str(self.pre_order())

    def __repr__(self):
        return f"PyAlStruct.BinarySearchTree({str(self)})"

    def __len__(self):
        return self._number_of_nodes

    @property
    def number_of_nodes(self) -> int:
        """
        Returns total number of nodes in the tree.
        :return: int -- The number of nodes in the tree.
        """
        return self._number_of_nodes

    @property
    def number_of_leafs(self) -> int:
        """
        Returns the number of leafs in the tree.
        :return: int -- The number of leafs in the tree.
        """
        def _number_of_leafs(node):
            if node is None:
                return 0
            if node.left is None and node.right is None:
                return 1
            return _number_of_leafs(node.left) + _number_of_leafs(node.right)
        return _number_of_leafs(self._root)

    @property
    def height(self) -> int:
        """
        Returns the height of the tree.
        :return: int -- The height of the tree.
        """
        def _height(node):
            if node is None:
                return 0
            return 1 + max(_height(node.left), _height(node.right))
        return _height(self._root)

    @property
    def min(self) -> Any:
        """
        Returns the minimum value in the tree.
        """
        temp: TreeNode = self._root
        while temp.left:
            temp = temp.left
        return temp.key

    @property
    def max(self) -> Any:
        """
        Returns the maximum value in the tree.
        """
        temp: TreeNode = self._root
        while temp.right:
            temp = temp.right
        return temp.key

    def is_empty(self) -> bool:
        """
        Check if the tree is empty.
        :returns: bool -- True if the tree is empty, otherwise False.
        """
        return self._root is None

    def pre_order(self) -> None:
        """
        Perform a preorder traversal of the binary search tree.
        """
        def _pre_order(node):
            if node:
                print(node.key, end=', ')
                _pre_order(node.left)
                _pre_order(node.right)
        if self._root is not None:
            _pre_order(self._root)
            print("end")

    def in_order(self) -> None:
        """
        Perform an inorder traversal of the binary search tree.
        """
        def _in_order(node):
            if node:
                _in_order(node.left)
                print(node.key, end=', ')
                _in_order(node.right)
        if self._root is not None:
            _in_order(self._root)
            print("end")

    def post_order(self) -> None:
        """
        Perform a postorder traversal of the binary search tree.
        """
        def _post_order(node):
            if node:
                _post_order(node.left)
                _post_order(node.right)
                print(node.key, end=', ')
        if self._root is not None:
            _post_order(self._root)
            print("end")

    def insert(self, key: Any) -> None:
        """
        Insert new key to the tree if it's not exist.
        :param key: the key to be inserted.
        """
        def _insert(root, _key) -> TreeNode:
            if root is None:
                return TreeNode(_key)
            if _key == root.key:
                raise ValueError(f'Key {_key} already exists')
            if _key < root.key:
                node = _insert(root.left, _key)
                root.left = node
                return root
            node = _insert(root.right, _key)
            root.right = node
            return root
        self._root = _insert(self._root, key)
        self._number_of_nodes += 1

    def get(self, key) -> TreeNode:
        """
        Return the node that contains key if exist in the tree.
        :param key: The key to search for.
        :return: TreeNode -- The node that contains key if exists, otherwise None.
        ":raises NodeNotFoundException if key is not found.
        """
        def _search(root, _key):
            if root is None:
                raise NodeNotFoundException(_key)
            if root.key == _key:
                return root
            if _key < root.key:
                return _search(root.left, _key)
            return _search(root.right, _key)
        return _search(self._root, key)

    def search(self, key) -> bool:
        """
        Search for a key in the tree.
        :param key: The key to search for.
        :return: bool -- True if key exists in the tree, otherwise False.
        """
        def _search(root, _key):
            if root is None:
                return False
            if root.key == _key:
                return True
            if _key < root.key:
                return _search(root.left, _key)
            return _search(root.right, _key)
        if self._root is None:
            return False
        return _search(self._root, key)

    def delete(self, key: Any) -> None:
        """
        Delete a key from the tree.
        :param key: The key to be added.
        """
        def _min_value_node(node: TreeNode) -> TreeNode:
            while node.left is not None:
                node: TreeNode = node.left
            return node

        def _max_value_node(node: TreeNode) -> TreeNode:
            while node.right is not None:
                node: TreeNode = node.right
            return node

        def _delete(root: TreeNode, _key: Any) -> TreeNode | None:
            if root is None:
                return root
            if _key < root.key:
                root.left = _delete(root.left, _key)
            elif _key > root.key:
                root.right = _delete(root.right, _key)
            else:
                if root.right is not None:
                    root.key = _min_value_node(root.right).key
                    root.right = _delete(root.right, root.key)
                elif root.left is not None:
                    root.key = _max_value_node(root.left).key
                    root.left = _delete(root.left, root.key)
                else:
                    root = None
            return root

        if self._root is None:
            raise EmptyTreeException()
        self._root = _delete(self._root, key)
        self._number_of_nodes -= 1
