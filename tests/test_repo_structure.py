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


COMMON_ZSH = REPO_ROOT / "private_dot_config" / "zsh" / "common.zsh"
CLI_TOOLS_SCRIPT = REPO_ROOT / ".chezmoiscripts" / "run_onchange_install-cli-tools.sh.tmpl"
TMUX_CONF = REPO_ROOT / "private_dot_config" / "tmux" / "tmux.conf"

TPM_SCRIPT = REPO_ROOT / ".chezmoiscripts" / "run_once_05-install-tpm.sh.tmpl"
TPM_DIR = "~/.tmux/plugins/tpm"
TMUX_PLUGINS_REQUIRED = [
    "tmux-plugins/tpm",
    "tmux-plugins/tmux-sensible",
    "tmux-plugins/tmux-resurrect",
    "tmux-plugins/tmux-continuum",
]

TMUX_CONF_REQUIRED = [
    "set -g prefix",
    "set -g mouse on",
    "set -g history-limit",
    "set -g base-index",
    "mode-keys vi",
    "set -g status",
    "source-file",          # reload binding
    "split-window -h",      # horizontal split
    "split-window -v",      # vertical split
]

# Tools that must appear in every package-manager block (brew, apt, dnf, pacman).
REQUIRED_CLI_TOOLS = ["tmux"]


def _extract_install_lines(text: str) -> list[str]:
    """Return lines that invoke a package manager or install helper."""
    keywords = ("install_brew", "install_apt", "install_pacman", "sudo dnf install")
    return [ln.strip() for ln in text.splitlines() if any(k in ln for k in keywords)]


def test_cli_tools_script_exists():
    assert CLI_TOOLS_SCRIPT.exists(), "CLI tools install script not found"


TMUX_ZSH_ALIASES = ["tm()", "tls=", "tks=", "td="]

# Aliases that must have inline comments (descriptions)
ALIASES_REQUIRING_COMMENTS = [
    "alias c=",
    "alias gs=",
    "alias cz=",
    "alias czd=",
    "alias cza=",
    "alias czu=",
    "alias cze=",
    "alias zshr=",
    "alias tls=",
    "alias tks=",
    "alias td=",
]


def test_common_zsh_has_tmux_aliases():
    text = COMMON_ZSH.read_text()
    for alias in TMUX_ZSH_ALIASES:
        assert alias in text, f"common.zsh missing tmux alias/function: {alias!r}"


def test_common_zsh_tmux_block_is_guarded():
    text = COMMON_ZSH.read_text()
    # tmux aliases must be inside a command -v tmux guard
    assert "command -v tmux" in text, "tmux aliases must be guarded by 'command -v tmux'"


def test_tpm_bootstrap_script_exists():
    assert TPM_SCRIPT.exists(), "TPM bootstrap script not found"


def test_tpm_bootstrap_is_idempotent():
    text = TPM_SCRIPT.read_text()
    assert ".git" in text, "TPM bootstrap must check for existing clone (idempotent)"


def test_tpm_bootstrap_clones_correct_repo():
    text = TPM_SCRIPT.read_text()
    assert "tmux-plugins/tpm" in text, "TPM bootstrap must clone tmux-plugins/tpm"


def test_tmux_conf_declares_required_plugins():
    text = TMUX_CONF.read_text()
    for plugin in TMUX_PLUGINS_REQUIRED:
        assert plugin in text, f"tmux.conf missing plugin declaration: {plugin!r}"


def test_tmux_conf_runs_tpm():
    text = TMUX_CONF.read_text()
    assert "run '~/.tmux/plugins/tpm/tpm'" in text, "tmux.conf must call TPM run at end"


def test_tmux_conf_exists():
    assert TMUX_CONF.exists(), "tmux.conf not found in private_dot_config/tmux/"
    assert TMUX_CONF.stat().st_size > 0, "tmux.conf is empty"


def test_tmux_conf_required_settings():
    text = TMUX_CONF.read_text()
    for setting in TMUX_CONF_REQUIRED:
        assert setting in text, f"tmux.conf missing required setting: {setting!r}"


def test_tmux_conf_no_machine_specific_paths():
    text = TMUX_CONF.read_text()
    forbidden = ["/home/", "/Users/", "/root/"]
    for path in forbidden:
        assert path not in text, f"tmux.conf contains machine-specific path: {path!r}"


CMDS_TXT = REPO_ROOT / "private_dot_config" / "zsh" / "cmds.txt"


def test_dotcmds_function_defined():
    text = COMMON_ZSH.read_text()
    assert "dotcmds()" in text, "common.zsh missing dotcmds() function"


def test_dotcmds_function_reads_common_zsh():
    text = COMMON_ZSH.read_text()
    assert "common.zsh" in text, "dotcmds() must reference common.zsh"


def test_dotcmds_function_supports_fzf_fallback():
    text = COMMON_ZSH.read_text()
    assert "command -v fzf" in text, "dotcmds() must check for fzf availability"


def test_dotcmds_function_supports_apps_mode():
    text = COMMON_ZSH.read_text()
    assert '"apps"' in text, "dotcmds() must support 'apps' keyword"


def test_cmds_txt_exists():
    assert CMDS_TXT.exists(), "cmds.txt not found in private_dot_config/zsh/"
    assert CMDS_TXT.stat().st_size > 0, "cmds.txt is empty"


def test_cmds_txt_entries_have_comments():
    entries = [
        ln for ln in CMDS_TXT.read_text().splitlines()
        if ln and not ln.startswith("#") and not ln.strip() == ""
    ]
    for entry in entries:
        assert "#" in entry, f"cmds.txt entry missing comment: {entry!r}"


CUSTOM_TOOLS_IN_CMDS = ["sshm", "local-env", "localz", "check-dotfiles"]


def test_cmds_txt_covers_custom_tools():
    text = CMDS_TXT.read_text()
    for tool in CUSTOM_TOOLS_IN_CMDS:
        assert tool in text, f"cmds.txt missing entries for custom tool: {tool!r}"


def test_cmds_txt_custom_tool_entries_have_category():
    text = CMDS_TXT.read_text()
    for tool in CUSTOM_TOOLS_IN_CMDS:
        tool_lines = [
            ln for ln in text.splitlines()
            if ln.startswith(tool) and "#" in ln
        ]
        assert tool_lines, f"cmds.txt has no documented commands for {tool!r}"
        for ln in tool_lines:
            assert f"# {tool}:" in ln, (
                f"cmds.txt entry for {tool!r} missing category prefix: {ln!r}"
            )


def test_dotcmds_function_reads_cmds_txt():
    text = COMMON_ZSH.read_text()
    assert "cmds.txt" in text, "dotcmds() must reference cmds.txt"


def test_aliases_have_inline_comments():
    text = COMMON_ZSH.read_text()
    for alias_prefix in ALIASES_REQUIRING_COMMENTS:
        matching = [ln for ln in text.splitlines() if alias_prefix in ln]
        assert matching, f"common.zsh missing alias: {alias_prefix!r}"
        for line in matching:
            assert "#" in line, (
                f"alias line missing inline comment: {line.strip()!r}"
            )


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
