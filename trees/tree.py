from trees.treeNode import TreeNode
from games.table import *

class Tree(object):
    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root is None

    def depth(self, x):
        if x.is_root():
            return 0
        else:
            return 1 + self.depth(x.parent)

    def _height(self, x):
        if x.is_leaf():
            return 0
        else:
            return 1 + max(self._height(c) for c in x.children)

    def height(self):
        return self._height(self.root)

