import unittest
from al_struct.utils import compare_nodes
from al_struct.utils.nodes import Node


class TestNode(unittest.TestCase):
    def test_node_creation(self):
        node = Node(42)
        self.assertEqual(node.data, 42)
        self.assertIsNone(node.next)

    def test_compare_two_nodes_equal(self):
        node1 = Node(10)
        node2 = Node(10)
        self.assertTrue(compare_nodes(node1, node2))

    def test_compare_two_nodes_not_equal(self):
        node1 = Node(10)
        node2 = Node(20)
        self.assertFalse(compare_nodes(node1, node2))

    def test_compare_nodes_with_next_equal(self):
        node1 = Node(10)
        node2 = Node(10)
        node3 = Node(20)
        node1.next = node3
        node2.next = node3
        self.assertTrue(compare_nodes(node1, node2))

    def test_compare_nodes_with_next_not_equal(self):
        node1 = Node(50)
        node2 = Node(50)
        node1.next = Node(60)
        node2.next = Node(70)
        self.assertFalse(compare_nodes(node1, node2))


if __name__ == '__main__':
    unittest.main()


def compare_structures(node1: Node, node2: Node) -> bool:
    """
    Compare two linked structures represented by nodes.

    :param node1: The head node of the first linked structure.
    :param node2: The head node of the second linked structure.
    :return: True if the linked structures are equal, False otherwise.
    """
    assert isinstance(node1, (Node, type(None))), "node1 should be a Node or None"
    assert isinstance(node2, (Node, type(None))), "node2 should be a Node or None"

    while compare_nodes(node1, node2):
        node1 = node1.next
        node2 = node2.next

    return node1 is None and node2 is None
