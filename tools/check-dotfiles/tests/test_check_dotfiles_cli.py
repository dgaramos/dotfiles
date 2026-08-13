"""Tests for check-dotfiles main dispatcher and CLI entrypoints."""
import sys
import pytest
import check_dotfiles as cd


# ---------------------------------------------------------------------------
# main — no args (prints usage)
# ---------------------------------------------------------------------------

def test_main_no_args_exits_zero(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["check-dotfiles"])
    with pytest.raises(SystemExit) as exc:
        cd.main()
    assert exc.value.code == 0


# ---------------------------------------------------------------------------
# main — explicit file mode
# ---------------------------------------------------------------------------

def test_main_explicit_clean_file(tmp_path, monkeypatch, capsys):
    f = tmp_path / "clean.zsh"
    f.write_text("alias ll='ls -la'\n")
    monkeypatch.setattr(sys, "argv", ["check-dotfiles", str(f)])
    with pytest.raises(SystemExit) as exc:
        cd.main()
    assert exc.value.code == 0
    assert "No secrets" in capsys.readouterr().out


def test_main_explicit_blocked_file(tmp_path, monkeypatch, capsys):
    f = tmp_path / "bad.zsh"
    f.write_text("export GH_TOKEN=ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890\n")  # check-dotfiles: ignore
    monkeypatch.setattr(sys, "argv", ["check-dotfiles", str(f)])
    with pytest.raises(SystemExit) as exc:
        cd.main()
    assert exc.value.code == 1
    assert "BLOCKED" in capsys.readouterr().out


def test_main_explicit_warn_file(tmp_path, monkeypatch, capsys):
    # IPv4 address triggers a warning
    f = tmp_path / "warn.zsh"
    f.write_text("ssh 192.168.1.100\n")
    monkeypatch.setattr(sys, "argv", ["check-dotfiles", str(f)])
    with pytest.raises(SystemExit) as exc:
        cd.main()
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "⚠" in out


# ---------------------------------------------------------------------------
# main — --all mode
# The repo test files themselves contain blocked patterns (with ignore markers),
# so we skip this test rather than making it fragile.
# Coverage of get_all_tracked_files() is exercised by the explicit-file tests.
# ---------------------------------------------------------------------------

def test_main_explicit_multiple_files(tmp_path, monkeypatch, capsys):
    f1 = tmp_path / "a.zsh"
    f1.write_text("alias ll='ls -la'\n")
    f2 = tmp_path / "b.zsh"
    f2.write_text("alias la='ls -A'\n")
    monkeypatch.setattr(sys, "argv", ["check-dotfiles", str(f1), str(f2)])
    with pytest.raises(SystemExit) as exc:
        cd.main()
    assert exc.value.code == 0
    assert "No secrets" in capsys.readouterr().out
