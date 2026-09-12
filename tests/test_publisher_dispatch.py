"""Verify the reviewer profile's publisher dispatch against installed workflows.

The profile declares which publisher workflow each dispatch mode uses, and
`.github/workflows/` holds the stubs actually installed. Those two must agree
in BOTH directions.

A forward-only check (declared -> installed) passes while an installed
publisher goes undeclared, which is precisely the drift that went unnoticed
here before. Both directions are therefore asserted separately, and each
failure names the offending file and the direction it drifted in.

This asserts only facts this repository owns: its own profile and its own
installed files. It deliberately does not assert catalog facts -- how many
publishers exist, or which modes require a catalog ref -- because those belong
to the catalog's own quality gate, not to this one.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PROFILE = REPO_ROOT / ".dr-agents" / "dotfiles" / "PROFILE.md"
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"

# A publisher stub filename is exactly `publish-<lowercase-token>.yml`. The
# pattern is strict on purpose: a file that looks like a stub but does not
# match this shape -- a name containing a space, for instance -- is not a name
# any profile could declare, so it belongs to neither direction and is neither
# counted nor reported. The anchor also excludes `reusable-publish-*.yml`,
# which stubs call and which are never dispatched as publishers themselves.
STUB_NAME = re.compile(r"^publish-[a-z0-9-]+\.yml$")

# Candidates are matched with a leading run of name characters so a token
# inside `reusable-publish-review.yml` yields the full name and is then
# rejected by the anchored filter, instead of matching the `publish-review.yml`
# substring and counting as a declaration.
CANDIDATE = re.compile(r"[a-z0-9-]*publish-[a-z0-9-]+\.yml")


def declared_publishers() -> set[str]:
    return {
        name
        for name in CANDIDATE.findall(PROFILE.read_text())
        if STUB_NAME.fullmatch(name)
    }


def installed_publishers() -> set[str]:
    return {
        path.name
        for path in WORKFLOWS_DIR.iterdir()
        if path.is_file() and STUB_NAME.fullmatch(path.name)
    }


def test_profile_and_workflows_directory_exist():
    assert PROFILE.is_file(), f"missing reviewer profile: {PROFILE}"
    assert WORKFLOWS_DIR.is_dir(), f"missing workflows directory: {WORKFLOWS_DIR}"


def test_publisher_sets_are_not_empty():
    """Guard against a silently-matching-nothing parser passing both directions."""
    assert declared_publishers(), "no publisher workflows declared in the profile"
    assert installed_publishers(), f"no publisher workflows installed in {WORKFLOWS_DIR}"


def test_every_declared_publisher_is_installed():
    missing = sorted(declared_publishers() - installed_publishers())
    assert not missing, "declared in profile but not installed in .github/workflows/: " + ", ".join(missing)


def test_every_installed_publisher_is_declared():
    undeclared = sorted(installed_publishers() - declared_publishers())
    assert not undeclared, "installed in .github/workflows/ but not declared in profile: " + ", ".join(undeclared)
