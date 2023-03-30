class SegmentTree:
    trees = []

    @classmethod
    def get_trees(cls):
        return cls.trees

    @classmethod
    def check_tree(cls, segment):
        for tree_object in cls.trees:
            for node in tree_object.tree:
                if segment in node:
                    return tree_object
        raise RuntimeWarning(f"Segment{segment} can't be found in trees.")

    def __init__(self, top):
        self.name = top.name
        self.tree = [[top, None], ]  # 映射集合，映射的第一个元素是父对象，第二个元素是子对象。
        SegmentTree.trees.append(self)

    def show(self, node=None, prefix='', last=True):
        # 如果是第一次调用，则将根节点作为起点
        if node is None:
            node = self.tree[0][0]
            print(node.name)

        # 获取当前节点的子节点列表
        subsegments = [x[1] for x in self.tree if x[0] == node]

        # 遍历子节点
        for i, subsegment in enumerate(subsegments):
            # 判断是否是最后一个子节点
            if i == len(subsegments) - 1:
                new_prefix = prefix + '`-- '
                new_last = True
            else:
                new_prefix = prefix + '|-- '
                new_last = False

            # 打印当前子节点的名字
            print(f'{new_prefix}{subsegment.name}')

            # 递归打印子节点的子节点
            self.show(subsegment, prefix + ('    ' if last else '|   '), new_last)

    def append_(self, subsegment, parent):
        if len(self.tree) == 1:
            self.tree.clear()
        self.tree.append([parent, subsegment])

    def get_parent(self, subsegment):
        for node in self.tree:
            if node[1] == subsegment:
                return node[0]
        raise ValueError(f"Failed to find parent of object {subsegment}.")

    def get_subsegments(self, parent):
        subsegments = []
        for node in self.tree:
            if node[0] == parent:
                subsegments.append(node[1])
                for _node in SegmentTree.get_subsegments(self, node[1]):
                    subsegments.append(_node)
        return subsegments


class SeriesTree:
    trees = []

    @classmethod
    def get_trees(cls):
        return cls.trees

    @classmethod
    def check_tree(cls, segment):
        for tree_object in cls.trees:
            for node in tree_object.tree:
                if segment in node:
                    return tree_object
        raise RuntimeWarning(f"Segment{segment} can't be found in trees.")

    def __init__(self, top):
        self.name = top.name
        self.tree = [[top, None], ]  # 映射集合，映射的第一个元素是父对象，第二个元素是子对象。
        SegmentTree.trees.append(self)

    def show(self, node=None, prefix='', last=True):
        # 如果是第一次调用，则将根节点作为起点
        if node is None:
            node = self.tree[0][0]
            print(node.name)

        # 获取当前节点的子节点列表
        subsegments = [x[1] for x in self.tree if x[0] == node]

        # 遍历子节点
        for i, subsegment in enumerate(subsegments):
            # 判断是否是最后一个子节点
            if i == len(subsegments) - 1:
                new_prefix = prefix + '`-- '
                new_last = True
            else:
                new_prefix = prefix + '|-- '
                new_last = False

            # 打印当前子节点的名字
            print(f'{new_prefix}{subsegment.name}')

            # 递归打印子节点的子节点
            self.show(subsegment, prefix + ('    ' if last else '|   '), new_last)

    def append_(self, subsegment, parent):
        if len(self.tree) == 1:
            self.tree.clear()
        self.tree.append([parent, subsegment])

    def get_parent(self, subsegment):
        for node in self.tree:
            if node[1] == subsegment:
                return node[0]
        raise ValueError(f"Failed to find parent of object {subsegment}.")

    def get_subsegments(self, parent):
        subsegments = []
        for node in self.tree:
            if node[0] == parent:
                subsegments.append(node[1])
                for _node in SegmentTree.get_subsegments(self, node[1]):
                    subsegments.append(_node)
        return subsegments


class RhymeTree:
    trees = []

    @classmethod
    def get_trees(cls):
        return cls.trees

    @classmethod
    def check_tree(cls, segment):
        for tree_object in cls.trees:
            for node in tree_object.tree:
                if segment in node:
                    return tree_object
        raise RuntimeWarning(f"Segment{segment} can't be found in trees.")

    def __init__(self, top):
        self.name = top.name
        self.tree = [[top, None], ]  # 映射集合，映射的第一个元素是父对象，第二个元素是子对象。
        SegmentTree.trees.append(self)

    def show(self, node=None, prefix='', last=True):
        # 如果是第一次调用，则将根节点作为起点
        if node is None:
            node = self.tree[0][0]
            print(node.name)

        # 获取当前节点的子节点列表
        subsegments = [x[1] for x in self.tree if x[0] == node]

        # 遍历子节点
        for i, subsegment in enumerate(subsegments):
            # 判断是否是最后一个子节点
            if i == len(subsegments) - 1:
                new_prefix = prefix + '`-- '
                new_last = True
            else:
                new_prefix = prefix + '|-- '
                new_last = False

            # 打印当前子节点的名字
            print(f'{new_prefix}{subsegment.name}')

            # 递归打印子节点的子节点
            self.show(subsegment, prefix + ('    ' if last else '|   '), new_last)

    def append_(self, subsegment, parent):
        if len(self.tree) == 1:
            self.tree.clear()
        self.tree.append([parent, subsegment])

    def get_parent(self, subsegment):
        for node in self.tree:
            if node[1] == subsegment:
                return node[0]
        raise ValueError(f"Failed to find parent of object {subsegment}.")

    def get_subsegments(self, parent):
        subsegments = []
        for node in self.tree:
            if node[0] == parent:
                subsegments.append(node[1])
                for _node in SegmentTree.get_subsegments(self, node[1]):
                    subsegments.append(_node)
        return subsegments
