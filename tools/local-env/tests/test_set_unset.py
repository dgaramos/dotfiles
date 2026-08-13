"""Tests for local-env set/unset/get commands."""
import local_env as le
import pytest


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(le, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(le, "ENV_FILE", tmp_path / "env")
    monkeypatch.setattr(le, "NAMES_FILE", tmp_path / "names")


def test_set_creates_env_file():
    le.cmd_set(["MY_VAR", "hello"])
    assert le.ENV_FILE.exists()


def test_set_and_get():
    le.cmd_set(["MY_VAR", "hello world"])
    assert le.read_vars()["MY_VAR"] == "hello world"


def test_set_registers_in_names():
    le.cmd_set(["MY_VAR", "value"])
    assert "MY_VAR" in le.read_names()


def test_unset_removes_from_env():
    le.cmd_set(["MY_VAR", "value"])
    le.cmd_unset(["MY_VAR"])
    assert "MY_VAR" not in le.read_vars()


def test_unset_keeps_name_in_registry():
    le.cmd_set(["MY_VAR", "value"])
    le.cmd_unset(["MY_VAR"])
    assert "MY_VAR" in le.read_names()


def test_unset_nonexistent_does_not_crash():
    le.cmd_unset(["NONEXISTENT_VAR"])
    assert "NONEXISTENT_VAR" in le.read_names()


def test_set_multiple_vars():
    le.cmd_set(["FOO", "1"])
    le.cmd_set(["BAR", "2"])
    vars_ = le.read_vars()
    assert vars_["FOO"] == "1"
    assert vars_["BAR"] == "2"


def test_invalid_name_raises():
    with pytest.raises(SystemExit):
        le.cmd_set(["123INVALID", "value"])


def test_get_existing():
    le.cmd_set(["MY_VAR", "hello"])
    vals = le.read_vars()
    assert vals["MY_VAR"] == "hello"


def test_get_missing_raises():
    with pytest.raises(SystemExit):
        le.cmd_get(["MISSING_VAR"])
