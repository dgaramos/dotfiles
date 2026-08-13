"""Tests for ~/.ssh/config parser."""
import sshm
import pytest


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(sshm, "SSH_DIR", tmp_path)
    monkeypatch.setattr(sshm, "SSH_CONFIG", tmp_path / "config")


def test_parse_empty_config():
    sshm.SSH_CONFIG.write_text("")
    blocks = sshm.parse_config()
    assert blocks == []


def test_parse_single_host():
    sshm.SSH_CONFIG.write_text(
        "Host myserver\n"
        "    HostName 10.0.0.1\n"
        "    User ec2-user\n"
    )
    blocks = sshm.parse_config()
    hosts = [b for b in blocks if b.get("host")]
    assert len(hosts) == 1
    assert hosts[0]["host"] == "myserver"
    assert sshm.get_option(hosts[0], "HostName") == "10.0.0.1"
    assert sshm.get_option(hosts[0], "User") == "ec2-user"


def test_parse_preserves_comments():
    content = "# global comment\nHost myserver\n    HostName 10.0.0.1\n"
    sshm.SSH_CONFIG.write_text(content)
    blocks = sshm.parse_config()
    raw_lines = [line for b in blocks for line in b["raw"]]
    assert any("# global comment" in l for l in raw_lines)


def test_parse_multiple_hosts():
    sshm.SSH_CONFIG.write_text(
        "Host server1\n    HostName 10.0.0.1\n\n"
        "Host server2\n    HostName 10.0.0.2\n"
    )
    blocks = sshm.parse_config()
    hosts = [b for b in blocks if b.get("host")]
    assert len(hosts) == 2


def test_write_config_roundtrip():
    content = "Host myserver\n    HostName 10.0.0.1\n    User ec2-user\n"
    sshm.SSH_CONFIG.write_text(content)
    blocks = sshm.parse_config()
    sshm.write_config(blocks)
    result = sshm.SSH_CONFIG.read_text()
    assert "Host myserver" in result
    assert "HostName 10.0.0.1" in result


def test_find_host_existing():
    sshm.SSH_CONFIG.write_text("Host myserver\n    HostName 10.0.0.1\n")
    blocks = sshm.parse_config()
    block = sshm.find_host(blocks, "myserver")
    assert block is not None


def test_find_host_missing():
    sshm.SSH_CONFIG.write_text("Host myserver\n    HostName 10.0.0.1\n")
    blocks = sshm.parse_config()
    assert sshm.find_host(blocks, "other") is None


def test_write_config_sets_permissions():
    import stat
    sshm.SSH_CONFIG.write_text("Host x\n    HostName 1.2.3.4\n")
    blocks = sshm.parse_config()
    sshm.write_config(blocks)
    mode = sshm.SSH_CONFIG.stat().st_mode
    assert stat.filemode(mode) == "-rw-------"
