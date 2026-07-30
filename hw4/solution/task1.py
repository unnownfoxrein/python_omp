class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinaryTree:
    def __init__(self, root=None):
        self.root = root

    def __iter__(self):
        raise NotImplementedError


class BinaryTreeIterator:
    def __init__(self, root):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


def inorder(node):
    raise NotImplementedError
