"""Verify that every tool directory has the required documentation files."""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
REQUIRED_FILES = {"README.md", "CLAUDE.md", "AGENTS.md"}


def tool_dirs():
    return [d for d in TOOLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]


def test_tools_dir_exists():
    assert TOOLS_DIR.is_dir()


def test_each_tool_has_bin():
    for tool in tool_dirs():
        bin_dir = tool / "bin"
        assert bin_dir.is_dir(), f"{tool.name}: missing bin/"
        executables = [f for f in bin_dir.iterdir() if f.is_file()]
        assert executables, f"{tool.name}: bin/ is empty"


def test_each_tool_has_required_docs():
    for tool in tool_dirs():
        for filename in REQUIRED_FILES:
            f = tool / filename
            assert f.exists(), f"{tool.name}: missing {filename}"
            assert f.stat().st_size > 0, f"{tool.name}: {filename} is empty"


def test_each_tool_bin_is_executable():
    for tool in tool_dirs():
        for f in (tool / "bin").iterdir():
            if f.is_file():
                assert f.stat().st_mode & 0o111, f"{tool.name}/{f.name}: not executable"


def test_version_file_exists():
    assert (TOOLS_DIR / ".version").exists()
    content = (TOOLS_DIR / ".version").read_text().strip()
    assert content.isdigit(), ".version must contain a single integer"


CLI_TOOLS_SCRIPT = REPO_ROOT / ".chezmoiscripts" / "run_onchange_install-cli-tools.sh.tmpl"

# Tools that must appear in every package-manager block (brew, apt, dnf, pacman).
REQUIRED_CLI_TOOLS = ["tmux"]


def _extract_install_lines(text: str) -> list[str]:
    """Return lines that invoke a package manager or install helper."""
    keywords = ("install_brew", "install_apt", "install_pacman", "sudo dnf install")
    return [ln.strip() for ln in text.splitlines() if any(k in ln for k in keywords)]


def test_cli_tools_script_exists():
    assert CLI_TOOLS_SCRIPT.exists(), "CLI tools install script not found"


def test_required_cli_tools_in_all_blocks():
    text = CLI_TOOLS_SCRIPT.read_text()
    install_lines = _extract_install_lines(text)
    assert install_lines, "No install lines found in CLI tools script"
    for tool in REQUIRED_CLI_TOOLS:
        matching = [ln for ln in install_lines if tool in ln]
        assert len(matching) >= 4, (
            f"'{tool}' must appear in all four package-manager blocks "
            f"(brew, apt, dnf, pacman); found only in: {matching}"
        )
