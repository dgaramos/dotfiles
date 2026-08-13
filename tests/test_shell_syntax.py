"""Verify that all managed zsh files load without syntax errors."""
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
ZSH_FILES = list((REPO_ROOT / "private_dot_config" / "zsh").rglob("*.zsh"))

pytestmark = pytest.mark.skipif(
    not shutil.which("zsh"), reason="zsh not available"
)


@pytest.mark.parametrize("zsh_file", ZSH_FILES, ids=lambda f: f.name)
def test_zsh_syntax(zsh_file):
    result = subprocess.run(
        ["zsh", "--no-rcs", "-n", str(zsh_file)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"{zsh_file.name} has syntax errors:\n{result.stderr}"
    )
