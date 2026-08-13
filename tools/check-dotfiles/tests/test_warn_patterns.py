"""Tests for patterns that warn but do not block."""
from conftest import scan


def test_ipv4_warns():
    _, warns = scan("ssh 10.0.0.42\n")
    assert any(w[1] == "ipv4-address" for w in warns)


def test_loopback_not_warned():
    _, warns = scan("host: 127.0.0.1\n")
    assert not any(w[1] == "ipv4-address" for w in warns)


def test_any_address_not_warned():
    _, warns = scan("bind: 0.0.0.0\n")
    assert not any(w[1] == "ipv4-address" for w in warns)


def test_documentation_range_not_warned():
    _, warns = scan("example: 192.0.2.1\n")
    assert not any(w[1] == "ipv4-address" for w in warns)


def test_ignore_marker_suppresses_warn():
    _, warns = scan("ssh 10.0.0.42  # check-dotfiles: ignore\n")
    assert warns == []
