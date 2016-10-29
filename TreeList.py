
# Brian Landes
# a structured list used for sorting objects

class TreeList(object):
    # takes values and pushes them into its nodes, where they're sorted
    def __init__(self):
        self.root = None
        pass

    def Put(self, value, data ):
        # takes a value for comparing and data for storing and returning
        if self.root is None:
            self.root = TreeNode( value, data, None )
        else:
            self.root.Put( value, data )

    def AsString(self):
        return self.root.AsString()

    def ToList(self,ascending=True):
        return self.root.ToList(ascending)

class TreeNode(object):
    def __init__(self, value, data, parent):
        self.value = value
        self.data = data
        self.left = None
        self.right = None
        self.parent = parent

    def Put(self, new_value, new_data ):
        # compares the new value against its own value and pushes it to either
        # the left or the right node
        if new_value < self.value:
            if self.left is None:
                # either create a new node where there wasn't one
                self.left = TreeNode(new_value, new_data, self)
            else:
                # or continue the push downwards through the node
                self.left.Put( new_value, new_data )
        else:
            # this will also catch equal-to, which is fine
            if self.right is None:
                self.right = TreeNode(new_value, new_data, self)
            else:
                self.right.Put(new_value, new_data)

    def AsString(self):
        s = ''
        if self.left is not None:
            s += self.left.AsString()
            s += ', '

        s += self.data

        if self.right is not None:
            s += ', '
            s += self.right.AsString()

        return s

    def ToList(self,ascending=True):
        values = []

        if ascending:
            if self.left is not None:
                values = values + self.left.ToList(ascending)
        else:
            if self.right is not None:
                values = values + self.right.ToList(ascending)


        values = values + [ self.data ]

        if ascending:
            if self.right is not None:
                values = values + self.right.ToList(ascending)
        else:
            if self.left is not None:
                values = values + self.left.ToList(ascending)

        return values

