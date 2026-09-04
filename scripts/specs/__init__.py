"""题目规格（一题一文件）。聚合导出 ALL，供脚本或工具使用。"""
import importlib.util
import pathlib
import sys


def _load(path):
    name = "spec_" + path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod.PROBLEM


ALL = []
for _f in sorted((pathlib.Path(__file__).parent / "algo").glob("*.py")):
    if _f.name == "__init__.py":
        continue
    ALL.append(_load(_f))
