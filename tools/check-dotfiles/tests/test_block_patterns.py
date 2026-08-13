"""Tests for patterns that block commits."""
from conftest import scan, scan_zsh


def test_private_key_rsa():
    blocks, _ = scan("-----BEGIN RSA PRIVATE KEY-----\nabc\n")  # check-dotfiles: ignore
    assert any(b[1] == "private-key" for b in blocks)


def test_private_key_openssh():
    blocks, _ = scan("-----BEGIN OPENSSH PRIVATE KEY-----\nabc\n")  # check-dotfiles: ignore
    assert any(b[1] == "private-key" for b in blocks)


def test_private_key_ec():
    blocks, _ = scan("-----BEGIN EC PRIVATE KEY-----\nabc\n")  # check-dotfiles: ignore
    assert any(b[1] == "private-key" for b in blocks)


def test_aws_access_key():
    blocks, _ = scan("export AWS_KEY=AKIAIOSFODNN7EXAMPLE\n")  # check-dotfiles: ignore
    assert any(b[1] == "aws-access-key" for b in blocks)


def test_github_token_ghp():
    blocks, _ = scan("TOKEN=ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890\n")  # check-dotfiles: ignore
    assert any(b[1] == "github-token" for b in blocks)


def test_github_token_gho():
    blocks, _ = scan("TOKEN=gho_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890\n")  # check-dotfiles: ignore
    assert any(b[1] == "github-token" for b in blocks)


def test_generic_password():
    blocks, _ = scan('password="supersecretvalue123"\n')  # check-dotfiles: ignore
    assert any(b[1] == "generic-token" for b in blocks)


def test_generic_api_key():
    blocks, _ = scan('api_key="abcdef1234567890"\n')  # check-dotfiles: ignore
    assert any(b[1] == "generic-token" for b in blocks)


def test_ec2_hostname():
    blocks, _ = scan("ssh ec2-13-216-20-162.compute-1.amazonaws.com\n")
    assert any(b[1] == "ec2-hostname" for b in blocks)


def test_external_service_alias_open_webui():
    blocks, _ = scan_zsh("alias owui='open-webui start'\n")
    assert any(b[1] == "external-service-alias" for b in blocks)


def test_external_service_alias_nginx():
    blocks, _ = scan_zsh("alias ng='nginx -s reload'\n")
    assert any(b[1] == "external-service-alias" for b in blocks)


def test_clean_content_passes():
    blocks, warns = scan('echo "hello world"\n')
    assert blocks == []
    assert warns == []


def test_ignore_marker_suppresses_block():
    blocks, _ = scan("export AWS_KEY=AKIAIOSFODNN7EXAMPLE  # check-dotfiles: ignore\n")
    assert blocks == []
