"""Verify that every tool directory has the required documentation files."""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
REQUIRED_FILES = {"README.md", "CLAUDE.md", "AGENTS.md"}


def tool_dirs():
    return [d for d in TOOLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]


def test_tools_dir_exists():
    assert TOOLS_DIR.is_dir()


def test_each_tool_has_bin():
    for tool in tool_dirs():
        bin_dir = tool / "bin"
        assert bin_dir.is_dir(), f"{tool.name}: missing bin/"
        executables = [f for f in bin_dir.iterdir() if f.is_file()]
        assert executables, f"{tool.name}: bin/ is empty"


def test_each_tool_has_required_docs():
    for tool in tool_dirs():
        for filename in REQUIRED_FILES:
            f = tool / filename
            assert f.exists(), f"{tool.name}: missing {filename}"
            assert f.stat().st_size > 0, f"{tool.name}: {filename} is empty"


def test_each_tool_bin_is_executable():
    for tool in tool_dirs():
        for f in (tool / "bin").iterdir():
            if f.is_file():
                assert f.stat().st_mode & 0o111, f"{tool.name}/{f.name}: not executable"


def test_version_file_exists():
    assert (TOOLS_DIR / ".version").exists()
    content = (TOOLS_DIR / ".version").read_text().strip()
    assert content.isdigit(), ".version must contain a single integer"
