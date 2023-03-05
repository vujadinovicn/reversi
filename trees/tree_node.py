class TreeNode(object):

    __slots__ = 'parent', 'children', 'data'

    def __init__(self, data):
        self.parent = None
        self.children = []
        self.data = data

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return len(self.children) == 0

    def add_child(self, x):
        x.parent = self
        self.children.append(x)

    def __str__(self):
        return str(self.data)