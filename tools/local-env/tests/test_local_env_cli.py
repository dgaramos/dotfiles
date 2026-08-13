"""Tests for local-env get, list, path, help, and main dispatcher."""
import sys
import local_env as le
import pytest


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(le, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(le, "ENV_FILE", tmp_path / "env")
    monkeypatch.setattr(le, "NAMES_FILE", tmp_path / "names")


# ---------------------------------------------------------------------------
# cmd_get
# ---------------------------------------------------------------------------

def test_get_prints_value(capsys):
    le.cmd_set(["MY_VAR", "hello"])
    capsys.readouterr()  # discard set output
    le.cmd_get(["MY_VAR"])
    assert capsys.readouterr().out.strip() == "hello"


def test_get_missing_raises():
    with pytest.raises(SystemExit):
        le.cmd_get(["NO_SUCH_VAR"])


def test_get_extra_args_raises():
    with pytest.raises(SystemExit):
        le.cmd_get(["MY_VAR", "extra"])


# ---------------------------------------------------------------------------
# cmd_list
# ---------------------------------------------------------------------------

def test_list_empty(capsys):
    le.cmd_list([])
    assert "No local environment" in capsys.readouterr().out


def test_list_shows_names(capsys):
    le.cmd_set(["FOO", "1"])
    le.cmd_set(["BAR", "2"])
    le.cmd_list([])
    out = capsys.readouterr().out
    assert "FOO" in out
    assert "BAR" in out


def test_list_extra_args_raises():
    with pytest.raises(SystemExit):
        le.cmd_list(["unexpected"])


# ---------------------------------------------------------------------------
# cmd_path
# ---------------------------------------------------------------------------

def test_path_prints_env_file(capsys):
    le.cmd_set(["X", "1"])
    capsys.readouterr()  # discard set output
    le.cmd_path([])
    out = capsys.readouterr().out.strip()
    assert out == str(le.ENV_FILE)


def test_path_extra_args_raises():
    with pytest.raises(SystemExit):
        le.cmd_path(["extra"])


# ---------------------------------------------------------------------------
# cmd_help
# ---------------------------------------------------------------------------

def test_help_prints_usage(capsys):
    le.cmd_help()
    out = capsys.readouterr().out
    assert "local-env set" in out


# ---------------------------------------------------------------------------
# main dispatcher
# ---------------------------------------------------------------------------

def test_main_no_args_prints_help(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["local-env"])
    le.main()
    assert "local-env set" in capsys.readouterr().out


def test_main_help_flag(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["local-env", "--help"])
    le.main()
    assert "local-env set" in capsys.readouterr().out


def test_main_set_and_get(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["local-env", "set", "MAIN_VAR", "42"])
    le.main()
    capsys.readouterr()  # discard set output
    monkeypatch.setattr(sys, "argv", ["local-env", "get", "MAIN_VAR"])
    le.main()
    assert capsys.readouterr().out.strip() == "42"


def test_main_unknown_command_raises(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["local-env", "bogus"])
    with pytest.raises(SystemExit):
        le.main()
