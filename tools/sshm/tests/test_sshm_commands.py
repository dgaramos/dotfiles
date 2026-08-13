"""Tests for sshm list_keys, cmd_list, derive_pubkey and cmd_edit."""
import sshm
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(sshm, "SSH_DIR", tmp_path)
    monkeypatch.setattr(sshm, "SSH_CONFIG", tmp_path / "config")


# ---------------------------------------------------------------------------
# list_keys
# ---------------------------------------------------------------------------

def test_list_keys_empty_dir():
    assert sshm.list_keys() == []


def test_list_keys_finds_pem():
    (sshm.SSH_DIR / "mykey.pem").write_text("fake")
    keys = sshm.list_keys()
    assert any(k.name == "mykey.pem" for k in keys)


def test_list_keys_finds_keypair():
    (sshm.SSH_DIR / "id_rsa").write_text("private")
    (sshm.SSH_DIR / "id_rsa.pub").write_text("public")
    keys = sshm.list_keys()
    assert any(k.name == "id_rsa" for k in keys)


def test_list_keys_excludes_pub_only():
    (sshm.SSH_DIR / "orphan.pub").write_text("public")
    keys = sshm.list_keys()
    assert not any(k.name == "orphan.pub" for k in keys)


def test_list_keys_ssh_dir_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(sshm, "SSH_DIR", tmp_path / "nonexistent")
    assert sshm.list_keys() == []


# ---------------------------------------------------------------------------
# cmd_list
# ---------------------------------------------------------------------------

def test_cmd_list_no_hosts(capsys):
    sshm.SSH_CONFIG.write_text("")
    sshm.cmd_list([])
    assert "No hosts" in capsys.readouterr().out


def test_cmd_list_shows_host(capsys):
    sshm.SSH_CONFIG.write_text(
        "Host myserver\n"
        "    HostName 10.0.0.1\n"
        "    User ec2-user\n"
        "    IdentityFile ~/.ssh/mykey.pem\n"
    )
    sshm.cmd_list([])
    out = capsys.readouterr().out
    assert "myserver" in out
    assert "10.0.0.1" in out
    assert "ec2-user" in out


def test_cmd_list_multiple_hosts(capsys):
    sshm.SSH_CONFIG.write_text(
        "Host alpha\n    HostName 10.0.0.1\n    User root\n\n"
        "Host beta\n    HostName 10.0.0.2\n    User admin\n"
    )
    sshm.cmd_list([])
    out = capsys.readouterr().out
    assert "alpha" in out
    assert "beta" in out


def test_cmd_list_no_config_file(capsys):
    # SSH_CONFIG does not exist — should behave as empty
    sshm.cmd_list([])
    assert "No hosts" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# derive_pubkey
# ---------------------------------------------------------------------------

def test_derive_pubkey_success():
    fake_key = "ssh-rsa AAAAB3NzaC1yc2E... user@host"
    with patch("sshm.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout=fake_key + "\n")
        result = sshm.derive_pubkey("/fake/path/key.pem")
    assert result == fake_key


def test_derive_pubkey_failure_raises():
    with patch("sshm.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stderr="Permission denied")
        with pytest.raises(SystemExit):
            sshm.derive_pubkey("/fake/path/key.pem")


# ---------------------------------------------------------------------------
# cmd_edit
# ---------------------------------------------------------------------------

def test_cmd_edit_opens_editor(monkeypatch):
    monkeypatch.setenv("EDITOR", "nano")
    with patch("sshm.subprocess.run") as mock_run:
        sshm.cmd_edit([])
    mock_run.assert_called_once()
    cmd = mock_run.call_args[0][0]
    assert cmd[0] == "nano"
    assert str(sshm.SSH_CONFIG) in cmd
