"""Tests for sshm cmd_add, cmd_copy_id, cmd_keygen and main dispatcher."""
import sys
import sshm
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(sshm, "SSH_DIR", tmp_path)
    monkeypatch.setattr(sshm, "SSH_CONFIG", tmp_path / "config")


def make_pem(tmp_path, name="mykey.pem"):
    p = tmp_path / name
    p.write_text("fake pem")
    p.chmod(0o400)
    return p


# ---------------------------------------------------------------------------
# cmd_add — no keys available, prompts for pem path
# ---------------------------------------------------------------------------

def test_cmd_add_no_keys(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    pem = outside / "mykey.pem"
    pem.write_text("fake pem")

    inputs = iter(["myhost", "1.2.3.4", "ec2-user", "22", str(pem), "n"])  # check-dotfiles: ignore
    with patch("builtins.input", side_effect=inputs):
        sshm.cmd_add([])

    blocks = sshm.parse_config()
    hosts = [b for b in blocks if b.get("host")]
    assert any(b["host"] == "myhost" for b in hosts)


def test_cmd_add_empty_alias_raises():
    inputs = iter([""])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            sshm.cmd_add([])


def test_cmd_add_empty_hostname_raises():
    inputs = iter(["myhost", ""])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            sshm.cmd_add([])


def test_cmd_add_duplicate_host_raises(tmp_path):
    sshm.SSH_CONFIG.write_text("Host myhost\n    HostName 1.2.3.4\n")  # check-dotfiles: ignore
    inputs = iter(["myhost"])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            sshm.cmd_add([])


def test_cmd_add_with_existing_key(tmp_path):
    pem = sshm.SSH_DIR / "mykey.pem"
    pem.write_text("fake pem")
    pem.chmod(0o400)

    inputs = iter(["myhost", "1.2.3.4", "ec2-user", "22", "n"])  # check-dotfiles: ignore
    with patch("builtins.input", side_effect=inputs), \
         patch("sshm.select_interactive", return_value="mykey.pem"):
        sshm.cmd_add([])

    blocks = sshm.parse_config()
    hosts = [b for b in blocks if b.get("host")]
    assert any(b["host"] == "myhost" for b in hosts)


def test_cmd_add_custom_key_path(tmp_path):
    pem = sshm.SSH_DIR / "existing.pem"
    pem.write_text("fake pem")
    pem.chmod(0o400)

    external = tmp_path / "external.pem"
    external.write_text("fake pem")

    inputs = iter(["myhost", "1.2.3.4", "ec2-user", "22", str(external), "n"])  # check-dotfiles: ignore
    with patch("builtins.input", side_effect=inputs), \
         patch("sshm.select_interactive", return_value=sshm.CUSTOM_SENTINEL):
        sshm.cmd_add([])

    blocks = sshm.parse_config()
    assert any(b["host"] == "myhost" for b in [b for b in blocks if b.get("host")])


def test_cmd_add_custom_port_written(tmp_path):
    pem = tmp_path / "outside" / "mykey.pem"
    pem.parent.mkdir()
    pem.write_text("fake pem")

    inputs = iter(["myhost", "1.2.3.4", "ec2-user", "2222", str(pem), "n"])  # check-dotfiles: ignore
    with patch("builtins.input", side_effect=inputs):
        sshm.cmd_add([])

    config = sshm.SSH_CONFIG.read_text()
    assert "Port 2222" in config


# ---------------------------------------------------------------------------
# cmd_copy_id
# ---------------------------------------------------------------------------

def test_cmd_copy_id_no_args_raises():
    with pytest.raises(SystemExit):
        sshm.cmd_copy_id([])


def test_cmd_copy_id_unknown_host_raises():
    sshm.SSH_CONFIG.write_text("")
    with pytest.raises(SystemExit):
        sshm.cmd_copy_id(["nonexistent"])


def test_cmd_copy_id_no_identity_raises():
    sshm.SSH_CONFIG.write_text("Host myhost\n    HostName 1.2.3.4\n")  # check-dotfiles: ignore
    with pytest.raises(SystemExit):
        sshm.cmd_copy_id(["myhost"])


def test_cmd_copy_id_pem_key(tmp_path):
    pem = sshm.SSH_DIR / "mykey.pem"
    pem.write_text("fake pem")
    sshm.SSH_CONFIG.write_text(
        "Host myhost\n"
        "    HostName 1.2.3.4\n"  # check-dotfiles: ignore
        "    User ec2-user\n"
        "    IdentityFile ~/.ssh/mykey.pem\n"
    )
    with patch("sshm.derive_pubkey", return_value="ssh-rsa AAAA"), \
         patch("sshm.subprocess.run") as mock_run:
        sshm.cmd_copy_id(["myhost"])
    mock_run.assert_called_once()


def test_cmd_copy_id_regular_key():
    sshm.SSH_CONFIG.write_text(
        "Host myhost\n"
        "    HostName 1.2.3.4\n"  # check-dotfiles: ignore
        "    IdentityFile ~/.ssh/id_rsa\n"
    )
    with patch("sshm.subprocess.run") as mock_run:
        sshm.cmd_copy_id(["myhost"])
    mock_run.assert_called_once()
    assert mock_run.call_args[0][0][0] == "ssh-copy-id"


# ---------------------------------------------------------------------------
# cmd_keygen
# ---------------------------------------------------------------------------

def test_cmd_keygen_generates_key():
    inputs = iter(["testkey", "ed25519", "test@host"])
    with patch("builtins.input", side_effect=inputs), \
         patch("sshm.subprocess.run") as mock_run:
        sshm.cmd_keygen([])
    mock_run.assert_called_once()
    cmd = mock_run.call_args[0][0]
    assert "ssh-keygen" in cmd


def test_cmd_keygen_existing_key_raises():
    existing = sshm.SSH_DIR / "id_ed25519"
    existing.write_text("exists")
    inputs = iter(["id_ed25519", "ed25519", ""])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            sshm.cmd_keygen([])


# ---------------------------------------------------------------------------
# main dispatcher
# ---------------------------------------------------------------------------

def test_main_help(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["sshm", "--help"])
    sshm.main()
    assert "sshm list" in capsys.readouterr().out


def test_main_no_args(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["sshm"])
    sshm.main()
    assert "sshm list" in capsys.readouterr().out


def test_main_list(capsys, monkeypatch):
    sshm.SSH_CONFIG.write_text("")
    monkeypatch.setattr(sys, "argv", ["sshm", "list"])
    sshm.main()
    assert "No hosts" in capsys.readouterr().out


def test_main_unknown_command_raises(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["sshm", "bogus"])
    with pytest.raises(SystemExit):
        sshm.main()
