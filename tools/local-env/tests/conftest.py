import importlib.machinery
import importlib.util
import sys
from pathlib import Path

_bin = Path(__file__).parent.parent / "bin" / "local-env"
spec = importlib.util.spec_from_loader(
    "local_env",
    importlib.machinery.SourceFileLoader("local_env", str(_bin)),
)
le = importlib.util.module_from_spec(spec)
spec.loader.exec_module(le)
sys.modules["local_env"] = le
