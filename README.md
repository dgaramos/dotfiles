# Dotfiles

<p align="center">

![chezmoi](https://img.shields.io/badge/chezmoi-dotfiles-blue)
![shell](https://img.shields.io/badge/shell-zsh-green)
![platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20EC2-lightgrey)
[![codecov](https://codecov.io/gh/dgaramos/dotfiles/graph/badge.svg)](https://codecov.io/gh/dgaramos/dotfiles)


</p>

Personal, reproducible shell environment managed with [chezmoi](https://www.chezmoi.io/).

This repository provides a portable developer workstation setup with shared shell improvements, automated CLI tooling installation, machine-specific configuration profiles, and support for machine-local configuration outside version control.

## Features

- Centralized ZSH configuration
- Cross-platform support (macOS, Linux, EC2, Steam Deck)
- Automated CLI installation
- Machine/profile separation
- Machine-local configuration via `local-env` and `local.zsh`
- Secret scanner pre-commit hook (`check-dotfiles`)
- SSH manager (`sshm`)
- Local shell manager (`localz`)
- Git identity managed per-machine via `local-env`
- bat and delta pre-configured
- tmux configured with persistent sessions (TPM, resurrect, continuum)
- Secret-safe — never commits credentials or private references
- Test suite for all custom tools
- `dotcmds` — in-shell command reference for aliases, functions, and CLI tools

## Supported Machines

| Machine | Profile | Role |
|---|---|---|
| Personal Mac | `personal` | `mac` |
| Work Mac | `work` | `work-mac` |
| Raspberry Pi | `personal` | `homelab` |
| Steam Deck | `personal` | `steamdeck` |
| EC2 (Amazon Linux) | `work` | `ec2` |

## Structure

```text
.
├── .chezmoi.yaml.tmpl
├── .chezmoiscripts/
├── .chezmoiignore
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── requirements-dev.txt
├── tests/                          ← integration tests (repo structure, shell syntax)
├── tools/                          ← custom CLI utilities
│   ├── check-dotfiles/
│   ├── local-env/
│   ├── localz/
│   └── sshm/
├── dot_zshrc.tmpl
└── private_dot_config/
    ├── bat/config
    ├── delta/config
    ├── starship.toml
    ├── tmux/tmux.conf
    └── zsh/
        ├── common.zsh
        ├── personal.zsh
        ├── work.zsh
        └── hosts/
            ├── mac.zsh
            ├── work-mac.zsh
            ├── homelab.zsh
            ├── steamdeck.zsh
            └── ec2.zsh
```

Each tool under `tools/` has its own `bin/`, `README.md`, `CLAUDE.md`, and `AGENTS.md`.

## Configuration Model

```text
.zshrc
├── common.zsh
├── profile
│   ├── personal.zsh
│   └── work.zsh
└── host
    ├── mac.zsh
    ├── work-mac.zsh
    ├── homelab.zsh
    ├── steamdeck.zsh
    └── ec2.zsh
```

Shared behavior belongs in `common.zsh`. Profile-specific in `personal.zsh` / `work.zsh`. Machine-specific in the corresponding host file.

Machine-local configuration that must not be synchronized is kept outside chezmoi.

## Custom Tools

| Tool | Description |
|---|---|
| `sshm` | Manage SSH hosts — add, list, copy keys, generate key pairs |
| `local-env` | Machine-local environment variables, outside chezmoi |
| `localz` | Manage `~/.config/zsh/local.zsh` |
| `check-dotfiles` | Secret scanner, runs as pre-commit hook |

Installed to `~/.local/bin/` via `run_onchange_install-tools.sh.tmpl`. See each tool's `README.md` for usage.

## Tooling

### Shell

- zsh-autosuggestions
- zsh-syntax-highlighting
- zsh-history-substring-search

### Navigation

- zoxide
- fzf

### Search

- ripgrep (`rgrep` alias)
- fd (`ff` alias)

POSIX `find` and `grep` are not replaced — shell tools and SDKs may depend on their standard behavior.

### File Viewing

- bat (`cat` alias)
- eza (`ll`, `tree` aliases)

### Git

- git-delta (side-by-side diffs, navigation)

### Terminal multiplexer

- tmux — configured via `private_dot_config/tmux/tmux.conf`
  - Prefix: `Ctrl+a`; mouse enabled; splits with `|` / `-`; pane navigation with `hjkl`
  - `tm [name]` — attach to session or create it (default: `main`)
  - `tls` / `tks` / `td` — list, kill, detach
  - [TPM](https://github.com/tmux-plugins/tpm) installed automatically via `run_once_05-install-tpm`
  - `tmux-resurrect` + `tmux-continuum` — sessions survive reboots and broken pipes

## Installation

### Prerequisites

The prompt uses [Starship](https://starship.rs) with icons that require a [Nerd Font](https://www.nerdfonts.com) in your terminal. On macOS:

```bash
brew install --cask font-jetbrains-mono-nerd-font
```

On remote machines (EC2, homelab) the font must be installed on the **client**, not the server.

### macOS

```bash
brew install chezmoi
chezmoi init <repository>
chezmoi apply
```

### Linux (one-liner)

```bash
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply <repository>
```

When prompted, enter the profile (`personal` or `work`) and role (`mac`, `work-mac`, `homelab`, `steamdeck`, or `ec2`).

### EC2 (Amazon Linux, Graviton/ARM64)

If `get.chezmoi.io` returns a 503, install chezmoi directly from GitHub:

```bash
curl -fLo /tmp/chezmoi.tar.gz https://github.com/twpayne/chezmoi/releases/download/v2.72.0/chezmoi_2.72.0_linux_arm64.tar.gz \
  && sudo tar -xzf /tmp/chezmoi.tar.gz -C /usr/local/bin chezmoi \
  && chezmoi init https://github.com/dgaramos/dotfiles.git \
  && rm -f ~/.local/share/chezmoi/.chezmoi.toml.tmpl \
  && chezmoi apply
```

When prompted, enter profile `work` and role `ec2`.

#### Known issues

| Problem | Cause | Fix |
|---|---|---|
| `get.chezmoi.io` returns 503 | Installer service unavailable | Use the direct GitHub release above |
| `multiple config file templates` | Legacy `.chezmoi.toml.tmpl` in source | `rm ~/.local/share/chezmoi/.chezmoi.toml.tmpl` then re-run |
| `multiple config files` | `.chezmoi.toml` and `.chezmoi.yaml` coexist | `rm ~/.config/chezmoi/chezmoi.toml` then `chezmoi apply` |
| `chsh: command not found` | Amazon Linux omits `chsh` by default | `sudo dnf install -y util-linux-user` |
| `zsh: command not found` after apply | chezmoi installed manually skips bootstrap | `sudo dnf install -y zsh` then `chezmoi apply` |

## Bootstrap Scripts

Scripts in `.chezmoiscripts/` run automatically during `chezmoi apply`:

```text
01-install-zsh          → installs zsh + sets as default shell (Linux only)
02-install-homebrew     → installs Homebrew (macOS only)
03-install-oh-my-zsh    → installs oh-my-zsh
04-install-zsh-plugins  → clones zsh plugins
05-install-tpm          → clones TPM into ~/.tmux/plugins/tpm
06-configure-gh-auth    → authenticates gh if available
07-configure-git        → sets git identity, wires delta config (macOS)
install-cli-tools       → installs CLI tools (re-runs when content changes)
install-git-hooks       → installs pre-commit scanner hook
install-tools           → installs custom tools from tools/ (re-runs on version bump)
```

All scripts are idempotent.

## Machine-local Configuration

```text
common.zsh
├── local-env       → machine-local environment variables
└── local.zsh       → other machine-local shell configuration
```

Use `local-env` for environment variables. Use `~/.config/zsh/local.zsh` as a generic escape hatch for local shell behavior.

Neither file is managed by chezmoi or committed.

The following paths are runtime state and never managed by chezmoi:

```text
~/.config/local-env/env      → local-env variable values
~/.config/local-env/names    → local-env variable names
~/.tmux/plugins/             → TPM and tmux plugins
```

## Command Reference (`dotcmds`)

The shell function `dotcmds` provides an in-shell reference for everything defined in these dotfiles.

```bash
dotcmds             # browse all aliases, functions and app commands via fzf
dotcmds apps        # show only app/tool commands (no aliases)
dotcmds tmux        # filter by keyword
dotcmds chezmoi     # filter chezmoi aliases
```

Aliases and functions defined in `common.zsh` must have an inline comment with the format `# category: description` — this is what `dotcmds` parses and displays.

App and tool commands are documented in:

```text
private_dot_config/zsh/cmds.txt
```

**When adding a new CLI tool or custom tool to the dotfiles, add its commands to `cmds.txt`** using the same format:

```text
tool <args>    # toolname: what it does
```

## Testing

```bash
pip install pytest   # or: brew install pytest
pytest tools/ tests/ -v
```

164 tests covering all custom tools, repo structure consistency, and zsh file syntax.

## Secrets

Never commit tokens, passwords, credentials, private keys, or authentication material. Machine-local values stay outside chezmoi. The `check-dotfiles` pre-commit hook enforces this automatically.

## Git Workflow

Conventional Commits — `type(scope): description`.

Allowed types: `feat`, `fix`, `docs`, `refactor`, `chore`, `test`, `build`, `ci`.

Before committing:

```bash
git diff && git status && chezmoi diff
pytest tools/ tests/
```

## License

MIT
