import importlib.machinery
import importlib.util
import sys
from pathlib import Path

_bin = Path(__file__).parent.parent / "bin" / "sshm"
spec = importlib.util.spec_from_loader(
    "sshm",
    importlib.machinery.SourceFileLoader("sshm", str(_bin)),
)
sshm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sshm)
sys.modules["sshm"] = sshm
