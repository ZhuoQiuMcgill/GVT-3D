class AddOnlyList:
    def __init__(self, elements=None):
        self._items = []
        if elements is not None:
            for e in elements:
                self._items.append(e)

    def append(self, item):
        self._items.append(item)

    def __str__(self):
        return str(self._items)

    def __getitem__(self, index):
        """允许通过索引访问，但不允许修改"""
        return self._items[index]

    def __len__(self):
        """返回列表长度"""
        return len(self._items)

    def __iter__(self):
        """允许迭代列表"""
        return iter(self._items)
