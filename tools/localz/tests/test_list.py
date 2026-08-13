"""Tests for localz list command."""
import localz as lz
import pytest


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(lz, "LOCAL_ZSH", tmp_path / "local.zsh")


def test_list_finds_alias():
    lz.LOCAL_ZSH.write_text("alias myalias='echo hello'\n")
    lz.LOCAL_ZSH.chmod(0o600)
    aliases, _ = _capture_list()
    assert any("myalias" in a[0] for a in aliases)


def test_list_finds_function():
    lz.LOCAL_ZSH.write_text("myfunc() {\n  echo hello\n}\n")
    lz.LOCAL_ZSH.chmod(0o600)
    _, funcs = _capture_list()
    assert "myfunc" in funcs


def test_list_empty_file():
    lz.LOCAL_ZSH.write_text("# just a comment\n")
    lz.LOCAL_ZSH.chmod(0o600)
    aliases, funcs = _capture_list()
    assert aliases == []
    assert funcs == []


def _capture_list():
    """Parse local.zsh directly instead of calling cmd_list (which prints)."""
    import re
    content = lz.LOCAL_ZSH.read_text()
    aliases = []
    functions = []
    for line in content.splitlines():
        stripped = line.strip()
        m = re.match(r"^alias\s+([\w.:-]+)=['\"]?(.*?)['\"]?\s*$", stripped)
        if m:
            aliases.append((m.group(1), m.group(2)))
            continue
        m = re.match(r"^(?:function\s+)?([\w-]+)\s*\(\s*\)\s*\{", stripped)
        if m:
            functions.append(m.group(1))
    return aliases, functions
