# Dotfiles

<p align="center">

![chezmoi](https://img.shields.io/badge/chezmoi-dotfiles-blue)
![shell](https://img.shields.io/badge/shell-zsh-green)
![platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20EC2-lightgrey)

</p>

Personal, reproducible shell environment managed with [chezmoi](https://www.chezmoi.io/).

This repository provides a portable developer workstation setup with shared shell improvements, automated CLI tooling installation, machine-specific configuration profiles, and support for machine-local configuration outside version control.

## Features

- Centralized ZSH configuration
- Cross-platform support
- Automated CLI installation
- Machine/profile separation
- Machine-local configuration
- Secret-safe configuration
- Reproducible workstation setup

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
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── dot_local/
│   └── bin/
│       └── executable_local-env
├── dot_zshrc.tmpl
└── private_dot_config/
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

## Configuration Model

Configuration is split into layers.

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

Shared behavior belongs in `common.zsh`.

Profile-specific behavior belongs in:

```text
personal.zsh
work.zsh
```

Machine-specific behavior belongs in the corresponding file under:

```text
~/.config/zsh/hosts/
```

Machine-local configuration that must not be synchronized is kept outside chezmoi.

## Tooling

### Shell

- zsh-autosuggestions
- zsh-syntax-highlighting
- zsh-history-substring-search

### Navigation

- zoxide
- fzf

### Search

- ripgrep
- fd

Aliases:

```text
ff     -> fd / fdfind
rgrep  -> ripgrep
```

POSIX commands such as `find` and `grep` are intentionally not replaced because shell tools and development SDKs may depend on their standard behavior.

### File Viewing

- bat
- eza

Aliases:

```text
cat   -> bat / batcat
ll    -> eza -lah
tree  -> eza --tree
```

### Git

Git output is enhanced with `git-delta`.

Features include:

- delta pager
- side-by-side diffs
- diff navigation

### Development

Depending on the machine:

- direnv
- SDKMAN
- NVM
- Java helpers
- Claude Code helpers

## Installation

### Prerequisites

The prompt uses [Starship](https://starship.rs) with icons that require a [Nerd Font](https://www.nerdfonts.com) installed in your terminal emulator. On macOS, install one with:

```bash
brew install --cask font-jetbrains-mono-nerd-font
```

Then set it as the font in your terminal preferences. On remote machines (EC2, homelab) the font must be installed on the **client** machine, not the server.

### macOS

```bash
brew install chezmoi
chezmoi init <repository>
chezmoi apply
```

### Linux (one-liner)

Installs chezmoi and applies the dotfiles in a single command — no GitHub login required:

```bash
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply <repository>
```

Replace `<repository>` with the GitHub repository URL or `owner/repo` shorthand.

When prompted, enter the profile (`personal` or `work`) and role (`mac`, `work-mac`, `homelab`, `steamdeck`, or `ec2`).

### Review changes

```bash
chezmoi diff
chezmoi status
```

## Bootstrap Scripts

Scripts in `.chezmoiscripts/` run automatically during `chezmoi apply` in alphabetical order. Numeric prefixes enforce the correct sequence:

```text
01-install-zsh         → installs zsh + sets as default shell (Linux only)
02-install-homebrew    → installs Homebrew (macOS only)
03-install-oh-my-zsh   → installs oh-my-zsh
04-install-zsh-plugins → clones zsh plugins
install-cli-tools      → installs CLI tools (re-runs when content changes)
```

All scripts are idempotent — safe to re-run on machines where dependencies are already installed.

## CLI Bootstrap

CLI tools are installed through chezmoi scripts.

Currently managed tools include:

- fzf
- zoxide
- ripgrep
- fd
- bat
- eza
- direnv
- delta
- starship
- gh

Package names are adapted when necessary for each platform.

### Debian

Some Debian packages use different executable names:

| Tool | Debian executable |
|---|---|
| `fd` | `fdfind` |
| `bat` | `batcat` |

The shell configuration handles these differences automatically.

### Amazon Linux (EC2)

Some tools use different package names on Amazon Linux:

| Tool | Package name |
|---|---|
| `fd` | `fd-find` |
| `delta` | `git-delta` |

The shell configuration handles these differences automatically.

### Steam Deck

SteamOS uses a read-only filesystem by default.

Package installation may require manually disabling read-only mode:

```bash
sudo steamos-readonly disable
```

This is intentionally not automated by the dotfiles.

## Machine-local Configuration

Some configuration belongs to a specific machine and should never be managed by chezmoi or committed to Git.

The shared `common.zsh` supports two machine-local mechanisms:

```text
common.zsh
├── local-env
│   └── machine-local environment variables
└── ~/.config/zsh/local.zsh
    └── other machine-local shell configuration
```

Use `local-env` for environment variables.

Use `~/.config/zsh/local.zsh` only as a generic escape hatch for local shell behavior that does not belong in the managed configuration.

Examples include:

- local aliases
- temporary shell initialization
- machine-specific functions
- dynamic integrations that should remain local

Create it with:

```bash
mkdir -p ~/.config/zsh
touch ~/.config/zsh/local.zsh
chmod 600 ~/.config/zsh/local.zsh
```

The file is loaded automatically by `common.zsh` when present.

> [!IMPORTANT]
> `~/.config/zsh/local.zsh` is intentionally not managed by chezmoi and must never be committed to this repository.

## local-env

The repository includes a `local-env` utility for managing machine-local environment variables.

It is versioned in:

```text
dot_local/bin/executable_local-env
```

and installed by chezmoi as:

```text
~/.local/bin/local-env
```

Only the tool is versioned. The values it manages remain local to each machine.

### Storage

`local-env` uses:

```text
~/.config/local-env/
├── env
└── names
```

`env` contains the currently configured environment variables.

Example:

```bash
# Managed by local-env.
# Machine-local values. Do not commit this file.

export API_URL=https://example.com
export PROJECT_NAME='My Project'
```

`names` is an internal registry of environment variable names that have been managed by `local-env`.

For example:

```text
API_URL
PROJECT_NAME
```

The registry is necessary because environment variables are inherited by child processes.

When a new shell starts, `common.zsh`:

1. reads `names`;
2. clears those variables from the inherited environment;
3. loads the current values from `env`;
4. loads `local.zsh` afterwards.

This means removing a variable with `local-env unset` also removes it correctly from subsequent shells without storing `unset VARIABLE` entries inside `env`.

Both files are machine-local runtime state and must never be added to chezmoi or committed.

### Commands

Set a value:

```bash
local-env set API_URL https://example.com
```

Set a value containing spaces:

```bash
local-env set PROJECT_NAME "My Project"
```

Read a value:

```bash
local-env get API_URL
```

List configured variable names:

```bash
local-env list
```

Remove a variable:

```bash
local-env unset API_URL
```

Show the storage path:

```bash
local-env path
```

Edit the environment file directly:

```bash
local-env edit
```

Show help:

```bash
local-env --help
```

### Machine isolation

Each machine has independent runtime state:

```text
dotfiles repository
└── local-env
        |
        ├── Personal Mac
        │   └── ~/.config/local-env/
        │       ├── env
        │       └── names
        |
        ├── Work Mac
        │   └── ~/.config/local-env/
        │       ├── env
        │       └── names
        |
        ├── Homelab
        │   └── ~/.config/local-env/
        │       ├── env
        │       └── names
        |
        ├── Steam Deck
        │   └── ~/.config/local-env/
        │       ├── env
        │       └── names
        |
        └── EC2
            └── ~/.config/local-env/
                ├── env
                └── names
```

The dotfiles synchronize the mechanism, not the machine-local values.

## Secrets

This repository must contain no secrets.

Never commit:

- API tokens
- passwords
- credentials
- private keys
- secret environment files
- authentication material

Machine-local values should remain outside chezmoi.

When possible, credentials should be retrieved from local credential stores or authenticated CLI tools instead of being written directly into files.

## Git Workflow

Commits use Conventional Commits.

Format:

```text
type(scope): description
```

Examples:

```text
feat(zsh): add machine-local environment manager
fix(zsh): clear inherited local environment variables
docs(readme): document local environment management
refactor(zsh): simplify local configuration
chore(repo): update metadata
```

Allowed types:

- `feat`
- `fix`
- `docs`
- `refactor`
- `chore`
- `test`
- `build`
- `ci`

Before committing:

```bash
git diff
git status
chezmoi diff
```

Keep commits small and focused.

## Roadmap

- Add secret-provider support
- Improve bootstrap validation
- Add automated checks
- Expand workstation automation
- Document recovery procedures

## License

MIT
