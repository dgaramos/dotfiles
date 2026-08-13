"""Tests for localz show, list output, and main dispatcher."""
import sys
import localz as lz
import pytest


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(lz, "LOCAL_ZSH", tmp_path / "local.zsh")


# ---------------------------------------------------------------------------
# cmd_show
# ---------------------------------------------------------------------------

def test_show_prints_file_contents(capsys):
    lz.LOCAL_ZSH.write_text("alias foo='bar'\n")
    lz.LOCAL_ZSH.chmod(0o600)
    lz.cmd_show()
    assert "alias foo='bar'" in capsys.readouterr().out


def test_show_creates_file_if_missing(capsys):
    lz.cmd_show()
    assert lz.LOCAL_ZSH.exists()


# ---------------------------------------------------------------------------
# cmd_list output
# ---------------------------------------------------------------------------

def test_list_prints_aliases(capsys):
    lz.LOCAL_ZSH.write_text("alias ll='ls -la'\n")
    lz.LOCAL_ZSH.chmod(0o600)
    lz.cmd_list()
    out = capsys.readouterr().out
    assert "ll" in out


def test_list_prints_functions(capsys):
    lz.LOCAL_ZSH.write_text("myfunc() {\n  echo hi\n}\n")
    lz.LOCAL_ZSH.chmod(0o600)
    lz.cmd_list()
    out = capsys.readouterr().out
    assert "myfunc" in out


def test_list_empty_prints_message(capsys):
    lz.LOCAL_ZSH.write_text("# just a comment\n")
    lz.LOCAL_ZSH.chmod(0o600)
    lz.cmd_list()
    assert "empty" in capsys.readouterr().out.lower()


# ---------------------------------------------------------------------------
# main dispatcher
# ---------------------------------------------------------------------------

def test_main_help(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["localz", "--help"])
    with pytest.raises(SystemExit):
        lz.main()
    assert "localz" in capsys.readouterr().out.lower()


def test_main_show(capsys, monkeypatch):
    lz.LOCAL_ZSH.write_text("alias x='y'\n")
    lz.LOCAL_ZSH.chmod(0o600)
    monkeypatch.setattr(sys, "argv", ["localz", "show"])
    lz.main()
    assert "alias x='y'" in capsys.readouterr().out


def test_main_list(capsys, monkeypatch):
    lz.LOCAL_ZSH.write_text("alias z='w'\n")
    lz.LOCAL_ZSH.chmod(0o600)
    monkeypatch.setattr(sys, "argv", ["localz", "list"])
    lz.main()
    assert "z" in capsys.readouterr().out


def test_main_add(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["localz", "add", "myalias", "echo hello"])
    lz.main()
    assert "alias myalias='echo hello'" in lz.LOCAL_ZSH.read_text()


def test_main_add_missing_args(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["localz", "add", "onlyname"])
    with pytest.raises(SystemExit):
        lz.main()


def test_main_unknown_command(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["localz", "bogus"])
    with pytest.raises(SystemExit):
        lz.main()
