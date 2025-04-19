class Tree:
    def __init__(self):
        self.parent = None

    def root(self):
        return self.parent.root() if self.parent else self

    def connected(self, tree):
        return self.root() == tree.root()

    def connect(self, tree):
        tree.root().parent = self
