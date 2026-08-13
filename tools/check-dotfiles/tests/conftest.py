import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch

_bin = Path(__file__).parent.parent / "bin" / "check-dotfiles"
spec = importlib.util.spec_from_loader(
    "check_dotfiles",
    importlib.machinery.SourceFileLoader("check_dotfiles", str(_bin)),
)
cd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cd)
sys.modules["check_dotfiles"] = cd


def scan(content: str, path: str = "test_file.txt"):
    """Scan a string as if it were a file at the given path."""
    p = Path(path)
    with patch.object(Path, "read_text", return_value=content), \
         patch.object(Path, "read_bytes", return_value=content.encode()):
        return cd.scan_file(p)


def scan_zsh(content: str, path: str = "private_dot_config/zsh/common.zsh"):
    """Scan a string as a zsh config file (enables alias checking)."""
    return scan(content, path)
