import pytest

from solution.task1 import BinaryTree, BinaryTreeIterator, Node, inorder


# --- Helper to build trees ---

def make_tree(*values):
    """Build a balanced-ish BST from sorted values for predictable in-order."""
    if not values:
        return None
    mid = len(values) // 2
    return Node(
        values[mid],
        make_tree(*values[:mid]),
        make_tree(*values[mid + 1:]),
    )


# --- Tests for BinaryTreeIterator (task 1a) ---

class TestBinaryTreeIterator:
    def test_empty_tree(self):
        it = BinaryTreeIterator(None)
        assert list(it) == []

    def test_single_node(self):
        it = BinaryTreeIterator(Node(42))
        assert list(it) == [42]

    def test_left_only(self):
        root = Node(3, Node(2, Node(1)))
        it = BinaryTreeIterator(root)
        assert list(it) == [1, 2, 3]

    def test_right_only(self):
        root = Node(1, None, Node(2, None, Node(3)))
        it = BinaryTreeIterator(root)
        assert list(it) == [1, 2, 3]

    def test_full_tree(self):
        root = Node(4, Node(2, Node(1), Node(3)), Node(6, Node(5), Node(7)))
        it = BinaryTreeIterator(root)
        assert list(it) == [1, 2, 3, 4, 5, 6, 7]

    def test_iterator_protocol(self):
        root = Node(1)
        it = BinaryTreeIterator(root)
        assert iter(it) is it

    def test_stop_iteration(self):
        it = BinaryTreeIterator(Node(1))
        next(it)
        with pytest.raises(StopIteration):
            next(it)

    @pytest.mark.parametrize("n", [5, 10, 20])
    def test_sorted_values(self, n):
        values = list(range(1, n + 1))
        root = make_tree(*values)
        it = BinaryTreeIterator(root)
        assert list(it) == values

    def test_zigzag_tree(self):
        root = Node(1, None, Node(3, Node(2)))
        it = BinaryTreeIterator(root)
        assert list(it) == [1, 2, 3]

    def test_partial_iteration(self):
        root = Node(2, Node(1), Node(3))
        it = BinaryTreeIterator(root)
        assert next(it) == 1
        assert next(it) == 2

    def test_duplicate_values(self):
        root = Node(2, Node(2, Node(1)), Node(2))
        it = BinaryTreeIterator(root)
        assert list(it) == [1, 2, 2, 2]


# --- Tests for inorder generator (task 1b) ---

class TestInorder:
    def test_empty(self):
        assert list(inorder(None)) == []

    def test_single_node(self):
        assert list(inorder(Node(42))) == [42]

    def test_left_only(self):
        root = Node(3, Node(2, Node(1)))
        assert list(inorder(root)) == [1, 2, 3]

    def test_right_only(self):
        root = Node(1, None, Node(2, None, Node(3)))
        assert list(inorder(root)) == [1, 2, 3]

    def test_full_tree(self):
        root = Node(4, Node(2, Node(1), Node(3)), Node(6, Node(5), Node(7)))
        assert list(inorder(root)) == [1, 2, 3, 4, 5, 6, 7]

    def test_is_generator(self):
        import types
        root = Node(1)
        gen = inorder(root)
        assert isinstance(gen, types.GeneratorType)

    @pytest.mark.parametrize("n", [5, 10, 20])
    def test_sorted_values(self, n):
        values = list(range(1, n + 1))
        root = make_tree(*values)
        assert list(inorder(root)) == values

    def test_zigzag_tree(self):
        root = Node(1, None, Node(3, Node(2)))
        assert list(inorder(root)) == [1, 2, 3]


# --- Tests for BinaryTree.__iter__ (integration) ---

class TestBinaryTreeIter:
    def test_empty_tree(self):
        tree = BinaryTree()
        assert list(tree) == []

    def test_full_tree(self):
        root = Node(4, Node(2, Node(1), Node(3)), Node(6, Node(5), Node(7)))
        tree = BinaryTree(root)
        assert list(tree) == [1, 2, 3, 4, 5, 6, 7]

    def test_repeated_iteration(self):
        root = Node(4, Node(2, Node(1), Node(3)), Node(6, Node(5), Node(7)))
        tree = BinaryTree(root)
        assert list(tree) == [1, 2, 3, 4, 5, 6, 7]
        assert list(tree) == [1, 2, 3, 4, 5, 6, 7]

    def test_for_loop(self):
        root = Node(2, Node(1), Node(3))
        tree = BinaryTree(root)
        result = []
        for val in tree:
            result.append(val)
        assert result == [1, 2, 3]

    def test_string_values(self):
        root = Node("b", Node("a"), Node("c"))
        tree = BinaryTree(root)
        assert list(tree) == ["a", "b", "c"]

    def test_iter_returns_generator(self):
        import types

        root = Node(1)
        tree = BinaryTree(root)
        assert isinstance(iter(tree), types.GeneratorType)
