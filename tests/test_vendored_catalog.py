"""Reject catalog files vendored into this repository.

The dr-agents catalog's ``core/`` tree was once copied here at the catalog's
own path (``core/issue-workflow/scripts/apply-pr-metadata.sh``). Nothing
installed it, nothing verified it, nothing ran it -- the reusable publishers
read the catalog checkout -- and it drifted from the catalog while chezmoi
deployed it into ``$HOME`` as ``~/core/...``.

This repository never owns a root ``core/`` directory, so any file under it is
a vendored catalog artifact. The failure lists every such file so the fix is
obvious. This asserts only a fact this repository owns: its own tree.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
VENDORED_ROOT = REPO_ROOT / "core"


def vendored_catalog_files() -> list[str]:
    if not VENDORED_ROOT.exists():
        return []
    return sorted(
        str(path.relative_to(REPO_ROOT))
        for path in VENDORED_ROOT.rglob("*")
        if path.is_file()
    )


def test_no_catalog_core_tree_is_vendored():
    found = vendored_catalog_files()
    assert not found, (
        "catalog core/ files vendored into this repository (nothing installs, "
        "verifies, or runs them; chezmoi would deploy them into $HOME): "
        + ", ".join(found)
    )
