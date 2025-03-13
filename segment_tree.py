# Segment tree implementation

'''
    Segment tree is a data structure that allows answering range queries over an array effectively, 
    while still being flexible enough to allow modifying the array. 
    This includes finding the sum of consecutive array elements a[l…r], 
    or finding the minimum element in a such a range in O(logn) time. 
    Between answering such queries the Segment tree allows modifying the array by replacing one element, 
    or even change the elements of a whole subsegment (e.g. assigning all elements a[l…r] to any value, 
    or adding a value to all element in a subsegment).    
'''

inf = 1e10

class SegmentTree:
    """数组实现自下而上遍历的线段树"""
    def __init__(self, data, treetype='sum'):
        self.n = len(data)
        # bit_length() = log2(n) + 1 if n > 0
        # 由于树的节点数是2的幂，所以我们需要找到大于等于n的最小2的幂
        self.size = 2 ** (self.n - 1).bit_length()
        print("tree size: ", (self.n - 1).bit_length(), self.size)
        self.treetype = treetype

        # 初始化树的节点数为2 * size，这样我们就可以使用1-based indexing
        if treetype == 'sum':
            self.tree = [0] * (2 * self.size)
        elif treetype == 'min':
            self.tree = [inf] * (2 * self.size)
        elif treetype == 'max':
            self.tree = [-inf] * (2 * self.size)

        # 将原始数据复制到树的叶子节点
        self.tree[self.size:self.size + self.n] = data
        
        # 从下到上构建加和树
        for i in range(self.size - 1, 0, -1):
            if treetype == 'sum':
                self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
            elif treetype == 'min':
                self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
            elif treetype == 'max':
                self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])

        print("tree: ", self.tree)

    
    def query(self, l, r):
        if l > r:
            return 0
        # 将l和r转换为叶子节点的索引
        l += self.size
        r += self.size

        # 初始化结果的初始值
        if self.treetype == 'sum':
            res = 0
        elif self.treetype == 'min':
            res = inf
        elif self.treetype == 'max':
            res = -inf
        
        # 从下到上遍历树
        while l <= r:
            if l % 2 == 1:
                if self.treetype == 'sum':
                    res += self.tree[l]
                elif self.treetype == 'min':
                    res = min(res, self.tree[l])
                elif self.treetype == 'max':
                    res = max(res, self.tree[l])
                l += 1
            if r % 2 == 0:
                if self.treetype == 'sum':
                    res += self.tree[r]
                elif self.treetype == 'min':
                    res = min(res, self.tree[r])
                elif self.treetype == 'max':
                    res = max(res, self.tree[r])
                r -= 1
            
            # 向上移动到父节点，其中每个父节点和子节点下标的关系是i//2
            l //= 2
            r //= 2
        return res

    def update(self, idx, value):
        idx += self.size
        self.tree[idx] = value
        idx //= 2
        while idx >= 1:
            new_val = self.tree[2 * idx] + self.tree[2 * idx + 1]
            if self.tree[idx] == new_val:
                break
            self.tree[idx] = new_val
            idx //= 2

# 示例用法
data = [1, 3, 5, 7, 9, 11]
st = SegmentTree(data,'min')
print(st.query(1, 4)) 
st.update(2, 10)
print(st.query(1, 3))