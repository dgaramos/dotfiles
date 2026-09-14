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


def vendored_catalog_files(repo_root: Path = REPO_ROOT) -> list[str]:
    vendored_root = repo_root / "core"
    if not vendored_root.exists():
        return []
    return sorted(
        str(path.relative_to(repo_root))
        for path in vendored_root.rglob("*")
        if path.is_file()
    )


def test_listing_names_every_vendored_file(tmp_path: Path):
    """The listing branch only runs when the guard fails, so exercise it on a
    scratch tree: a guard whose failure path nothing executes is unproven."""
    (tmp_path / "core" / "issue-workflow" / "scripts").mkdir(parents=True)
    (tmp_path / "core" / "issue-workflow" / "scripts" / "apply-pr-metadata.sh").write_text("#!/bin/sh\n")
    (tmp_path / "core" / "other.md").write_text("x\n")
    (tmp_path / "core" / "empty-dir").mkdir()
    assert vendored_catalog_files(tmp_path) == [
        "core/issue-workflow/scripts/apply-pr-metadata.sh",
        "core/other.md",
    ]


def test_listing_is_empty_without_a_core_tree(tmp_path: Path):
    assert vendored_catalog_files(tmp_path) == []


def test_no_catalog_core_tree_is_vendored():
    found = vendored_catalog_files()
    assert not found, (
        "catalog core/ files vendored into this repository (nothing installs, "
        "verifies, or runs them; chezmoi would deploy them into $HOME): "
        + ", ".join(found)
    )
