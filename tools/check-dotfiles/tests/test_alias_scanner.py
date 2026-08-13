"""Tests for alias scanning in zsh config files."""
from conftest import scan, scan_zsh


def test_repo_installed_alias_passes():
    blocks, warns = scan_zsh("alias s='sshm list'\n")
    assert blocks == []
    assert not any(w[1] == "uninstalled-alias" for w in warns)


def test_system_command_alias_passes():
    blocks, warns = scan_zsh("alias ll='ls -la'\n")
    assert blocks == []
    assert not any(w[1] == "uninstalled-alias" for w in warns)


def test_unknown_command_warns():
    _, warns = scan_zsh("alias myapp='totally-unknown-binary start'\n")
    assert any(w[1] == "uninstalled-alias" for w in warns)


def test_guarded_unknown_command_does_not_warn():
    content = "if command -v myapp >/dev/null 2>&1; then\nalias myapp='myapp start'\nfi\n"
    _, warns = scan_zsh(content)
    assert not any(w[1] == "uninstalled-alias" for w in warns)


def test_alias_not_scanned_outside_zsh_config():
    blocks, warns = scan("alias myapp='open-webui start'\n", path="README.md")
    assert not any(b[1] == "external-service-alias" for b in blocks)
    assert not any(w[1] == "uninstalled-alias" for w in warns)


def test_fzf_alias_passes():
    blocks, warns = scan_zsh("alias fzp='fzf --preview'\n")
    assert blocks == []
    assert not any(w[1] == "uninstalled-alias" for w in warns)
