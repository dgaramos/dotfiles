"""Tests for file format, permissions, and shlex quoting."""
import local_env as le
import pytest
import stat


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(le, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(le, "ENV_FILE", tmp_path / "env")
    monkeypatch.setattr(le, "NAMES_FILE", tmp_path / "names")


def test_env_file_has_correct_permissions():
    le.cmd_set(["MY_VAR", "value"])
    mode = le.ENV_FILE.stat().st_mode
    assert stat.filemode(mode) == "-rw-------"


def test_names_file_has_correct_permissions():
    le.cmd_set(["MY_VAR", "value"])
    mode = le.NAMES_FILE.stat().st_mode
    assert stat.filemode(mode) == "-rw-------"


def test_config_dir_has_correct_permissions():
    le.cmd_set(["MY_VAR", "value"])
    mode = le.CONFIG_DIR.stat().st_mode
    assert oct(mode)[-3:] == "700"


def test_value_with_spaces_quoted():
    le.cmd_set(["MY_VAR", "hello world"])
    content = le.ENV_FILE.read_text()
    assert "export MY_VAR='hello world'" in content


def test_value_roundtrips_correctly():
    le.cmd_set(["MY_VAR", "hello world"])
    assert le.read_vars()["MY_VAR"] == "hello world"


def test_special_chars_roundtrip():
    le.cmd_set(["MY_VAR", "it's a test"])
    assert le.read_vars()["MY_VAR"] == "it's a test"


def test_env_file_format():
    le.cmd_set(["MY_VAR", "value"])
    lines = le.ENV_FILE.read_text().splitlines()
    export_lines = [l for l in lines if l.startswith("export ")]
    assert all("=" in l for l in export_lines)


def test_names_sorted():
    le.cmd_set(["ZZZ", "1"])
    le.cmd_set(["AAA", "2"])
    names_content = le.NAMES_FILE.read_text().splitlines()
    assert names_content == sorted(names_content)
