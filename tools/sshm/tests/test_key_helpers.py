"""Tests for .pem key helpers."""
import sshm
import pytest
import stat


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(sshm, "SSH_DIR", tmp_path)
    monkeypatch.setattr(sshm, "SSH_CONFIG", tmp_path / "config")


def test_install_pem_copies_file(tmp_path):
    src = tmp_path / "outside" / "mykey.pem"
    src.parent.mkdir()
    src.write_text("fake pem content")
    dst = sshm.install_pem(src)
    assert dst == sshm.SSH_DIR / "mykey.pem"
    assert dst.exists()


def test_install_pem_sets_permissions(tmp_path):
    src = tmp_path / "outside" / "mykey.pem"
    src.parent.mkdir()
    src.write_text("fake pem content")
    dst = sshm.install_pem(src)
    assert stat.filemode(dst.stat().st_mode) == "-r--------"


def test_install_pem_already_in_ssh_dir():
    existing = sshm.SSH_DIR / "mykey.pem"
    existing.write_text("fake pem content")
    existing.chmod(0o644)
    dst = sshm.install_pem(existing)
    assert dst == existing
    assert stat.filemode(dst.stat().st_mode) == "-r--------"


def test_install_pem_missing_file_raises():
    with pytest.raises(SystemExit):
        sshm.install_pem("/nonexistent/path/key.pem")
