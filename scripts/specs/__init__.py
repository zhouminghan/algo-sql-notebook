"""所有算法题规格聚合。每个 batch 模块导出 PROBLEMS 列表。"""
from .batch1 import PROBLEMS as _b1
from .batch2 import PROBLEMS as _b2
from .batch3 import PROBLEMS as _b3
from .batch4 import PROBLEMS as _b4
from .batch5 import PROBLEMS as _b5
from .batch6 import PROBLEMS as _b6

ALL = _b1 + _b2 + _b3 + _b4 + _b5 + _b6
