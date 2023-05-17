class Tree:

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
        if len(self.tree) == 1 and self.tree[0][1] is None:
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


class SegmentTree(Tree):
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
        raise RuntimeWarning(f"Segment {segment.segment} could not be found in trees.")

    def __init__(self, top):
        super().__init__(top)
        self.name = top.name
        self.tree = [[top, None], ]  # 映射集合，映射的第一个元素是父对象，第二个元素是子对象。
        SegmentTree.trees.append(self)


class SeriesTree(Tree):
    trees = []

    @classmethod
    def get_trees(cls):
        return cls.trees

    @classmethod
    def check_tree(cls, series):
        for tree_object in cls.trees:
            for node in tree_object.tree:
                if series in node:
                    return tree_object
        print(cls.trees)
        raise RuntimeWarning(f"PitchSeries {series.series} can't be found in trees.")

    def __init__(self, top):
        super().__init__(top)
        self.name = top.name
        self.tree = [[top, None], ]  # 映射集合，映射的第一个元素是父对象，第二个元素是子对象。
        SegmentTree.trees.append(self)


class RhythmTree(Tree):
    trees = []

    @classmethod
    def get_trees(cls):
        return cls.trees

    @classmethod
    def check_tree(cls, rhythm):
        for tree_object in cls.trees:
            for node in tree_object.tree:
                if rhythm in node:
                    return tree_object
        raise RuntimeWarning(f"Segment{rhythm} can't be found in trees.")

    def __init__(self, top):
        super().__init__(top)
        self.name = top.name
        self.tree = [[top, None], ]  # 映射集合，映射的第一个元素是父对象，第二个元素是子对象。
        SegmentTree.trees.append(self)


class PitchClassSeriesTree(Tree):
    trees = []

    @classmethod
    def get_trees(cls):
        return cls.trees

    @classmethod
    def check_tree(cls, pitch_class_series):
        for tree_object in cls.trees:
            for node in tree_object.tree:
                if pitch_class_series in node:
                    return tree_object
        raise RuntimeWarning(f"Pitch-class series {pitch_class_series} can't be found in trees.")

    def __init__(self, top):
        super().__init__(top)
        self.name = top.name
        self.tree = [[top, None], ]  # 映射集合，映射的第一个元素是父对象，第二个元素是子对象。
        SegmentTree.trees.append(self)


class MainTree:
    def __init__(self):
        self.series_trees = SeriesTree.trees
        self.rhythm_trees = RhythmTree
        self.segment_trees = SegmentTree.trees
