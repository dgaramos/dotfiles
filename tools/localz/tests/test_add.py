"""Tests for localz add command."""
import localz as lz
import pytest


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(lz, "LOCAL_ZSH", tmp_path / "local.zsh")


def test_add_creates_file():
    lz.cmd_add("myalias", "echo hello")
    assert lz.LOCAL_ZSH.exists()


def test_add_writes_alias():
    lz.cmd_add("myalias", "echo hello")
    content = lz.LOCAL_ZSH.read_text()
    assert "alias myalias='echo hello'" in content


def test_add_duplicate_raises():
    lz.cmd_add("myalias", "echo hello")
    with pytest.raises(SystemExit):
        lz.cmd_add("myalias", "echo world")


def test_add_multiple_aliases():
    lz.cmd_add("foo", "echo foo")
    lz.cmd_add("bar", "echo bar")
    content = lz.LOCAL_ZSH.read_text()
    assert "alias foo=" in content
    assert "alias bar=" in content


def test_file_permissions():
    lz.cmd_add("myalias", "echo hello")
    import stat
    mode = lz.LOCAL_ZSH.stat().st_mode
    assert stat.filemode(mode) == "-rw-------"


def test_new_file_has_header():
    lz.cmd_add("myalias", "echo hello")
    content = lz.LOCAL_ZSH.read_text()
    assert content.startswith("#")
