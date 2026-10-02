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


def test_decky_update_does_not_use_reserved_zsh_parameters(tmp_path):
    steamdeck_zsh = (
        REPO_ROOT / "private_dot_config" / "zsh" / "hosts" / "steamdeck.zsh"
    )
    script = f"""
source {steamdeck_zsh!s}
curl() {{
    print -r -- '#!/bin/sh\n[ -x "$0" ]' > "${{@[-1]}}"
}}
decky_update
"""
    result = subprocess.run(
        ["zsh", "--no-rcs", "-c", script],
        capture_output=True,
        text=True,
        env={"HOME": str(tmp_path), "TMPDIR": str(tmp_path), "PATH": "/usr/bin:/bin"},
    )
    assert result.returncode == 0, result.stderr
