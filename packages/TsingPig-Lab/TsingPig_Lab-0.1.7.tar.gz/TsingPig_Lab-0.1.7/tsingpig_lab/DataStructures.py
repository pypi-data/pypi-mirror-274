import math
from math import *
from typing import List


class ST:
    def __init__(self, nums: List, opt = lambda a, b: max(a, b)):
        """
        初始化稀疏表（ST）数据结构，使用给定的数字列表和可选的比较函数。

        :param nums: 预处理的数字列表。
        :param opt: 用于查询的比较函数。默认为 max。
        """
        n = len(nums)
        log = [0] * (n + 1)
        for i in range(2, n + 1):
            log[i] = log[i >> 1] + 1
        lenj = ceil(math.log(n, 2)) + 1
        f = [[0] * lenj for _ in range(n)]
        for i in range(n):
            f[i][0] = nums[i]
        for j in range(1, lenj):
            for i in range(n + 1 - (1 << j)):
                f[i][j] = opt(f[i][j - 1], f[i + (1 << (j - 1))][j - 1])
        self.__f = f
        self.__log = log
        self.__opt = opt

    def qry(self, L: int, R: int):
        """
        查询范围 [L, R] 内的最大值。

        :param L: 范围的左索引。
        :param R: 范围的右索引。
        :return: 范围 [L, R] 内的最大值。
        :rtype: object
        """
        k = self.__log[R - L + 1]
        return self.__opt(self.__f[L][k], self.__f[R - (1 << k) + 1][k])


class FenwickTree:
    def __lowbit(self, x: int) -> int:
        """
        返回x 的二进制中，最低为的1所构成的数。
        :param x: 整数
        :return: x的二进制中，最低为的1所构成的数
        """
        return x & -x

    def __init__(self, n: int, discretize: bool = False, nums: [List[int]] = None):
        """
        初始化树状数组（Fenwick Tree）数据结构，下标从0开始
        :param n: 数组长度
        :param discretize: 是否对输入值进行离散化
        :param nums: 离散化所需的输入数组
        """
        self.__dic = None
        self.__discretize = discretize
        self.__nums = None
        self.__n = n

        if discretize:
            unique_nums = sorted(set(nums))
            self.__dic = {unique_nums[i]: i + 1 for i in range(len(unique_nums))}
            self.__n = len(unique_nums)

        self.__nums = [0] * (self.__n + 1)

    def __query(self, x: int) -> int:
        """
        查询小于等于x的个数
        :param x: 查询的数
        :return: 查询小于等于x的个数
        """
        res = 0
        while x > 0:
            res += self.__nums[x]
            x -= self.__lowbit(x)
        return res

    def update(self, x: int, val: int = 1) -> None:
        """
        x处对应的值增加val
        :param x: 更新的数
        :param val: 变化值
        """
        if self.__discretize:
            if x not in self.__dic:
                raise ValueError(f"值{x} 不在离散化范围内")
            x = self.__dic[x]

        while x <= self.__n:
            self.__nums[x] += val
            x += self.__lowbit(x)

    def query(self, lx: int, rx: int = None) -> int:
        """
        如果只传入一个参数，则查询小于等于lx的个数
        如果传入两个参数，则查询大于等于lx, 小于等于rx的个数
        :param lx: 查询区间左端点
        :param rx: 查询区间右端点
        :return: 查询区间内的元素个数
        """
        if self.__discretize:
            if lx not in self.__dic:
                raise ValueError(f"值{lx} 不在离散化范围内")
            lx = self.__dic[lx]
            if rx is not None:
                if rx not in self.__dic:
                    raise ValueError(f"值{rx} 不在离散化范围内")
                rx = self.__dic[rx]

        if rx is not None:
            if lx > rx:
                raise ValueError(f"左边界{lx} 大于右边界{rx}")
            return self.__query(rx) - self.__query(lx - 1)
        return self.__query(lx)


class SegmentTree:
    """
    线段树数据结构，支持不同操作类型的线段树构建和区间查询。
    """

    __slots__ = ['node', 'lazy', 'n', 'nums', 'op', 'ini', 'ops']

    def __init__(self, nums, ops = 'sum'):
        """
        初始化线段树。

        :param nums: 初始数据数组。
        :param ops: 操作类型，支持'sum'、'bin'、'max'和'min'，分别表示求和、二进制操作、最大值和最小值。默认为'sum'。
        """
        n = len(nums)
        if ops == 'sum' or ops == 'bin':
            op, ini = lambda a, b: a + b, 0
        elif ops == 'max':
            op, ini = lambda a, b: max(a, b), float('-inf')
        elif ops == 'min':
            op, ini = lambda a, b: min(a, b), float('inf')
        self.nums = nums
        self.op = op
        self.ini = ini
        self.ops = ops
        self.node = [ini] * (4 * n)
        self.lazy = [None] * (4 * n)
        self.n = n

    def build(self, idx = 1, l = 1, r = None):
        """
        构建线段树。

        :param idx: 当前节点索引。
        :param l: 当前节点表示的区间左端点。
        :param r: 当前节点表示的区间右端点。
        """
        if r is None: r = self.n
        if l == r:
            self.node[idx] = self.nums[l - 1]
            return
        mid = (l + r) >> 1
        self.build(idx << 1, l, mid)
        self.build((idx << 1) + 1, mid + 1, r)
        self.node[idx] = self.op(self.node[idx << 1], self.node[(idx << 1) + 1])

    def __do(self, idx, dl, dr, val = None):
        """
        执行延迟更新或标记操作。

        :param idx: 当前节点索引。
        :param dl: 当前节点表示的区间左端点。
        :param dr: 当前节点表示的区间右端点。
        :param val: 要更新的值。
        """
        if self.ops == 'bin':
            self.node[idx] = dr - dl + 1
            self.lazy[idx] = True
        else:
            self.node[idx] = self.op(val, self.node[idx])
            self.lazy[idx] = val

    def __pushdown(self, idx, pl, pr):
        """
        执行延迟更新操作。

        :param idx: 当前节点索引。
        :param pl: 当前节点表示的区间左端点。
        :param pr: 当前节点表示的区间右端点。
        """
        val = self.lazy[idx]
        mid = (pl + pr) >> 1
        self.__do(idx << 1, pl, mid, val)
        self.__do((idx << 1) + 1, mid + 1, pr, val)
        self.lazy[idx] = None

    def update(self, ul, ur, val, idx = 1, l = 1, r = None):
        """
        更新线段树的区间值。

        :param ul: 区间左端点。
        :param ur: 区间右端点。
        :param val: 更新值。
        :param idx: 当前节点索引。
        :param l: 当前节点表示的区间左端点。
        :param r: 当前节点表示的区间右端点。
        """
        if r is None: r = self.n
        if ul <= l and r <= ur:
            self.__do(idx, l, r, val)
            return
        if self.lazy[idx]:
            self.__pushdown(idx, l, r)
        mid = (l + r) >> 1
        if ul <= mid: self.update(ul, ur, val, idx << 1, l, mid)
        if ur > mid: self.update(ul, ur, val, (idx << 1) + 1, mid + 1, r)
        self.node[idx] = self.op(self.node[idx << 1], self.node[(idx << 1) + 1])

    def query(self, ql, qr, idx = 1, l = 1, r = None):
        """
        查询线段树的区间值。

        :param ql: 查询区间左端点。
        :param qr: 查询区间右端点。
        :param idx: 当前节点索引。
        :param l: 当前节点表示的区间左端点。
        :param r: 当前节点表示的区间右端点。
        :return: 查询区间的结果值。
        """
        if r is None: r = self.n
        if ql <= l and r <= qr:
            return self.node[idx]
        if self.lazy[idx]:
            self.__pushdown(idx, l, r)
        mid = (l + r) >> 1
        ansl, ansr = self.ini, self.ini
        if ql <= mid: ansl = self.query(ql, qr, idx << 1, l, mid)
        if qr > mid: ansr = self.query(ql, qr, (idx << 1) + 1, mid + 1, r)
        return self.op(ansl, ansr)
