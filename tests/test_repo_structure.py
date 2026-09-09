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


FONTS_SCRIPT = REPO_ROOT / ".chezmoiscripts" / "run_once_06-install-fonts.sh.tmpl"
ITERM2_PROFILE = REPO_ROOT / "Library" / "Application Support" / "iTerm2" / "DynamicProfiles" / "dotfiles.json"


def test_fonts_script_exists():
    assert FONTS_SCRIPT.is_file(), "run_once_06-install-fonts.sh.tmpl is missing"


def test_fonts_script_covers_macos():
    text = FONTS_SCRIPT.read_text()
    assert "brew" in text and "font-fira-code-nerd-font" in text, (
        "fonts script must install via Homebrew on macOS"
    )


def test_fonts_script_covers_linux():
    text = FONTS_SCRIPT.read_text()
    assert "install_firacode_nerd_font_linux" in text, (
        "fonts script must include a Linux install path"
    )


def test_iterm2_profile_exists():
    assert ITERM2_PROFILE.is_file(), "iTerm2 DynamicProfiles/dotfiles.json is missing"


def test_iterm2_profile_is_valid_json():
    import json
    json.loads(ITERM2_PROFILE.read_text())


def test_iterm2_profile_uses_firacode_nerd_font():
    import json
    profiles = json.loads(ITERM2_PROFILE.read_text())["Profiles"]
    assert any("FiraCode" in p.get("Normal Font", "") for p in profiles), (
        "iTerm2 profile must set FiraCode Nerd Font"
    )


def test_iterm2_profile_enables_ligatures():
    import json
    profiles = json.loads(ITERM2_PROFILE.read_text())["Profiles"]
    assert any(p.get("Use Ligatures") is True for p in profiles), (
        "iTerm2 profile must have Use Ligatures: true"
    )


def test_install_sh_exists():
    install_sh = REPO_ROOT / "install.sh"
    assert install_sh.exists(), "install.sh missing at repository root"
    assert install_sh.stat().st_size > 0, "install.sh is empty"
    assert install_sh.stat().st_mode & 0o111, "install.sh is not executable"


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


# --- Documentation contract: standalone install + release versioning ---------

INSTALL_URL = (
    "https://github.com/dgaramos/dotfiles/releases/latest/download/install.sh"
)


def _readme_text():
    return (REPO_ROOT / "README.md").read_text()


def _agents_text():
    return (REPO_ROOT / "AGENTS.md").read_text()


def _section(text, heading):
    """Return the body of the section introduced by `heading`, or ''."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().lower() == heading.strip().lower():
            level = len(line) - len(line.lstrip("#"))
            body = []
            in_fence = False
            for nxt in lines[i + 1:]:
                if nxt.lstrip().startswith("```"):
                    in_fence = not in_fence
                elif not in_fence and nxt.startswith("#"):
                    if len(nxt) - len(nxt.lstrip("#")) <= level:
                        break
                body.append(nxt)
            return "\n".join(body)
    return ""


def test_readme_documents_standalone_tool_install():
    section = _section(_readme_text(), "## Installation")
    assert section, "README.md has no '## Installation' section"
    assert INSTALL_URL in section, (
        "README Installation section must document the release install.sh URL"
    )
    assert "bash -s -- sshm" in section, (
        "README Installation section must show the single-tool install form"
    )


def test_readme_documents_python3_requirement():
    section = _section(_readme_text(), "## Installation")
    assert "Python 3" in section, (
        "README Installation section must state that Python 3 is required "
        "on the target machine"
    )


def test_agents_md_documents_release_versioning():
    assert _section(_agents_text(), "### Release versioning"), (
        "AGENTS.md must have a '### Release versioning' section"
    )


def test_agents_md_distinguishes_version_files():
    section = _section(_agents_text(), "### Release versioning")
    assert "`version`" in section, (
        "Release versioning section must name the root `version` file"
    )
    assert "`tools/.version`" in section, (
        "Release versioning section must name `tools/.version` as distinct"
    )
    assert "release workflow" in section.lower(), (
        "Release versioning section must state `version` is updated by the "
        "release workflow"
    )


def test_readme_documents_release_trigger():
    section = _section(_readme_text(), "## Releases")
    assert section, "README.md must have a '## Releases' section"
    assert ".github/workflows/release.yml" in section, (
        "Releases section must name the release workflow file"
    )
    assert "main" in section and "push" in section.lower(), (
        "Releases section must state the workflow runs on every push to main"
    )
    assert "pytest tools/ tests/" in section, (
        "Releases section must state the test job gates the release"
    )


def test_readme_documents_release_assets():
    section = _section(_readme_text(), "## Releases")
    for asset in ("sshm", "local-env", "localz", "check-dotfiles", "install.sh"):
        assert asset in section, f"Releases section must list asset '{asset}'"


def test_readme_documents_release_notes_grouping():
    section = _section(_readme_text(), "## Releases")
    for group in ("Features", "Bug Fixes", "Documentation", "Refactors",
                  "Tests", "Chores", "Other"):
        assert group in section, (
            f"Releases section must list release-note group '{group}'"
        )


def test_agents_md_documents_version_bump_rules():
    section = _section(_agents_text(), "### Release versioning")
    for rule in ("BREAKING CHANGE", "major", "minor", "patch"):
        assert rule in section, (
            f"Release versioning section must document the '{rule}' bump rule"
        )
    assert "[skip ci]" in section, (
        "Release versioning section must document the automated bump commit"
    )
    assert "github-actions[bot]" in section, (
        "Release versioning section must name the committing bot"
    )


# --- Release workflow contract: notes quality + docs-only skip ---------------

RELEASE_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "release.yml"
NON_RELEASABLE_TYPES = ("docs", "chore", "ci", "build", "test")


def _release_workflow_text():
    return RELEASE_WORKFLOW.read_text()


def _workflow_job(name):
    """Return the body of the top-level job `name` from release.yml, or ''."""
    lines = _release_workflow_text().splitlines()
    header = f"  {name}:"
    for i, line in enumerate(lines):
        if line.rstrip() == header:
            body = []
            for nxt in lines[i + 1:]:
                if nxt.strip() and not nxt.startswith("    "):
                    break
                body.append(nxt)
            return "\n".join(body)
    return ""


def test_release_workflow_exists():
    assert RELEASE_WORKFLOW.is_file(), "missing .github/workflows/release.yml"


def test_release_gate_job_is_defined():
    assert _workflow_job("gate"), (
        "release.yml must define a 'gate' job that decides whether a release "
        "is cut"
    )


def test_gate_job_outputs_should_release():
    job = _workflow_job("gate")
    assert "outputs:" in job and "should_release" in job, (
        "the gate job must expose a 'should_release' output"
    )


def test_release_job_is_conditional_on_the_gate():
    job = _workflow_job("release")
    assert "needs:" in job and "gate" in job, (
        "the release job must depend on the gate job"
    )
    assert "needs.gate.outputs.should_release" in job, (
        "the release job must be skipped via an 'if:' on the gate output"
    )


def test_test_job_is_not_gated():
    job = _workflow_job("test")
    assert "should_release" not in job, (
        "the test job must keep running even when no release is cut"
    )


def test_gate_treats_docs_and_chore_ranges_as_non_releasable():
    job = _workflow_job("gate")
    for commit_type in NON_RELEASABLE_TYPES:
        assert commit_type in job, (
            f"the gate job must classify '{commit_type}' commits as "
            "non-releasable"
        )


def test_gate_still_releases_breaking_changes():
    job = _workflow_job("gate")
    assert "BREAKING CHANGE" in job and "!:" in job, (
        "a breaking commit must release even when its type is non-releasable"
    )


def test_gate_logs_an_explicit_skip_reason():
    job = _workflow_job("gate")
    assert "No release" in job, (
        "the gate job must print an explicit message stating why no release "
        "was cut"
    )


def test_release_notes_emit_a_breaking_changes_section():
    text = _release_workflow_text()
    assert "## BREAKING CHANGES" in text, (
        "release notes must include a dedicated '## BREAKING CHANGES' section"
    )


def test_breaking_changes_section_is_listed_first():
    text = _release_workflow_text()
    breaking = text.index("## BREAKING CHANGES")
    for later in ("## Features", "## Bug Fixes", "## Other"):
        assert breaking < text.index(later), (
            f"'## BREAKING CHANGES' must be assembled before '{later}'"
        )


def test_release_notes_exclude_merge_commits():
    text = _release_workflow_text()
    assert "--no-merges" in text, (
        "release notes must exclude merge commits with git log --no-merges"
    )


def test_release_notes_link_each_entry_to_its_commit():
    text = _release_workflow_text()
    assert "%H" in text, "the notes step must capture the commit hash"
    assert "/commit" in text and "${COMMIT_URL}/${HASH}" in text, (
        "each release-note entry must link to its commit URL"
    )
    assert "rev | cut -d' ' -f2- | rev" not in text, (
        "the notes step must no longer strip and discard the commit hash"
    )


def test_readme_documents_release_notes_improvements():
    section = _section(_readme_text(), "## Releases")
    assert "BREAKING CHANGES" in section, (
        "Releases section must document the BREAKING CHANGES group"
    )
    assert "merge commit" in section.lower(), (
        "Releases section must state that merge commits are excluded"
    )
    assert "link" in section.lower(), (
        "Releases section must state that entries link to their commit"
    )


def test_readme_documents_when_no_release_is_cut():
    section = _section(_readme_text(), "## Releases")
    for commit_type in NON_RELEASABLE_TYPES:
        assert f"`{commit_type}`" in section, (
            f"Releases section must list '{commit_type}' as non-releasable"
        )
    assert "test` job" in section, (
        "Releases section must state the test job still runs when the "
        "release is skipped"
    )


def test_agents_md_documents_the_release_skip_rule():
    section = _section(_agents_text(), "### Release versioning")
    assert "skip" in section.lower(), (
        "Release versioning section must document that some ranges cut no "
        "release"
    )
    for commit_type in NON_RELEASABLE_TYPES:
        assert f"`{commit_type}`" in section, (
            f"Release versioning section must list '{commit_type}' as "
            "non-releasable"
        )


# --- _section() helper contract ---------------------------------------------

def test_section_returns_empty_for_a_missing_heading():
    doc = "# Title\n\nsome text\n\n## Present\n\nbody\n"
    assert _section(doc, "## Absent") == ""


def test_section_ignores_hashes_inside_fenced_code_blocks():
    doc = (
        "## Target\n"
        "before\n"
        "```bash\n"
        "# this is a shell comment, not a heading\n"
        "echo hi\n"
        "```\n"
        "after\n"
        "## Next\n"
        "excluded\n"
    )
    section = _section(doc, "## Target")
    assert "before" in section
    assert "echo hi" in section
    assert "after" in section, (
        "a '#' comment inside a fenced block must not terminate the section"
    )
    assert "excluded" not in section


def test_section_stops_at_a_same_level_heading():
    doc = "## Target\nkept\n## Sibling\ndropped\n"
    section = _section(doc, "## Target")
    assert "kept" in section and "dropped" not in section


def test_section_stops_at_a_higher_level_heading():
    doc = "## Target\nkept\n# Parent\ndropped\n"
    section = _section(doc, "## Target")
    assert "kept" in section and "dropped" not in section


def test_section_includes_deeper_subheadings():
    doc = "## Target\nkept\n### Child\nalso kept\n## Sibling\ndropped\n"
    section = _section(doc, "## Target")
    assert "kept" in section
    assert "### Child" in section and "also kept" in section, (
        "a deeper heading must not terminate the section"
    )
    assert "dropped" not in section


def test_workflow_job_returns_empty_for_a_missing_job():
    assert _workflow_job("no-such-job") == ""
