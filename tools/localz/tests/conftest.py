import importlib.machinery
import importlib.util
import sys
from pathlib import Path

_bin = Path(__file__).parent.parent / "bin" / "localz"
spec = importlib.util.spec_from_loader(
    "localz",
    importlib.machinery.SourceFileLoader("localz", str(_bin)),
)
lz = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lz)
sys.modules["localz"] = lz
