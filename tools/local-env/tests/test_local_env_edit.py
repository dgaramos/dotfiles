"""Tests for local-env cmd_edit and parser edge cases."""
import local_env as le
import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(le, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(le, "ENV_FILE", tmp_path / "env")
    monkeypatch.setattr(le, "NAMES_FILE", tmp_path / "names")


# ---------------------------------------------------------------------------
# cmd_edit
# ---------------------------------------------------------------------------

def test_cmd_edit_opens_editor(monkeypatch):
    le.ensure_storage()
    monkeypatch.setenv("EDITOR", "vim")
    with patch("local_env.subprocess.run") as mock_run:
        mock_run.return_value = None
        le.cmd_edit([])
    mock_run.assert_called_once()
    assert mock_run.call_args[0][0][0] == "vim"


def test_cmd_edit_syncs_names_after_manual_edit(monkeypatch):
    le.cmd_set(["EXISTING", "value"])
    le.ENV_FILE.write_text("export EXISTING='value'\nexport NEW_VAR='added'\n")
    with patch("local_env.subprocess.run"):
        le.cmd_edit([])
    names = le.read_names()
    assert "EXISTING" in names
    assert "NEW_VAR" in names


def test_cmd_edit_extra_args_raises():
    with pytest.raises(SystemExit):
        le.cmd_edit(["unexpected"])


# ---------------------------------------------------------------------------
# Parser edge cases
# ---------------------------------------------------------------------------

def test_read_vars_skips_blank_lines():
    le.ENV_FILE.write_text("\nexport FOO='bar'\n\n")
    le.ENV_FILE.chmod(0o600)
    assert le.read_vars()["FOO"] == "bar"


def test_read_vars_skips_comments():
    le.ENV_FILE.write_text("# comment\nexport FOO='bar'\n")
    le.ENV_FILE.chmod(0o600)
    assert le.read_vars()["FOO"] == "bar"


def test_read_vars_skips_invalid_name():
    le.ENV_FILE.write_text("export 123INVALID='val'\nexport OK='yes'\n")
    le.ENV_FILE.chmod(0o600)
    result = le.read_vars()
    assert "123INVALID" not in result
    assert result["OK"] == "yes"


def test_read_vars_line_without_export_prefix():
    le.ENV_FILE.write_text("FOO='bar'\n")
    le.ENV_FILE.chmod(0o600)
    assert le.read_vars()["FOO"] == "bar"
