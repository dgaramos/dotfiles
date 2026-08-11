# Dotfiles

<p align="center">

![chezmoi](https://img.shields.io/badge/chezmoi-dotfiles-blue)
![shell](https://img.shields.io/badge/shell-zsh-green)
![platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey)

</p>

Personal, reproducible shell environment managed with chezmoi.

This repository provides a portable developer workstation setup with
shared shell improvements, automated CLI tooling installation, and
machine-specific configuration profiles.

## Features

-   Centralized ZSH configuration
-   Cross-platform support
-   Automated CLI installation
-   Machine/profile separation
-   Secret-safe configuration
-   Reproducible workstation setup

## Supported Machines

  Machine        Profile    Role
  -------------- ---------- -----------
  Personal Mac   personal   mac
  Work Mac       work       work-mac
  Raspberry Pi   personal   homelab
  Steam Deck     personal   steamdeck

## Structure

``` text
.
├── .chezmoi.toml.tmpl
├── .chezmoiscripts/
├── dot_zshrc.tmpl
└── private_dot_config/
    └── zsh/
        ├── common.zsh
        ├── personal.zsh
        ├── work.zsh
        └── hosts/
```

## Tooling

### Shell

-   zsh-autosuggestions
-   zsh-syntax-highlighting
-   zsh-history-substring-search

### Navigation

-   zoxide
-   fzf

### Search

-   ripgrep
-   fd

Aliases:

``` text
ff -> fd/fdfind
rgrep -> ripgrep
```

### File Viewing

-   bat
-   eza

Aliases:

``` text
cat -> bat/batcat
ll -> eza -lah
tree -> eza --tree
```

### Git

Powered by git-delta:

-   delta pager
-   side-by-side diff
-   navigation

### Development

-   direnv
-   SDKMAN
-   NVM
-   Java helpers

## Installation

Install chezmoi:

``` bash
brew install chezmoi
```

Initialize:

``` bash
chezmoi init <repository>
chezmoi apply
```

Review:

``` bash
chezmoi diff
chezmoi status
```

## Platform Notes

Debian compatibility:

  Tool   Debian name
  ------ -------------
  fd     fdfind
  bat    batcat

Steam Deck:

``` bash
sudo steamos-readonly disable
```

## Secrets

This repository contains no secrets.

Never commit:

-   API tokens
-   passwords
-   private keys
-   credential files
-   secret .env files

## Machine-local configuration

Some environment variables or machine-specific values should exist only on a single machine and must not be managed by chezmoi.

For the Work Mac, `hosts/work-mac.zsh` loads an optional local file:

```zsh
if [[ -f "$HOME/.config/zsh/local.zsh" ]]; then
    source "$HOME/.config/zsh/local.zsh"
fi
```

Create it directly on the machine:

```bash
mkdir -p ~/.config/zsh
touch ~/.config/zsh/local.zsh
chmod 600 ~/.config/zsh/local.zsh
```

Use this file for local-only environment variables and sensitive configuration:

```zsh
export SOME_LOCAL_VARIABLE="value"
```

For credentials that can be retrieved dynamically, prefer using the system credential store or CLI authentication instead of storing the secret value directly.

Example:

```zsh
if command -v gh >/dev/null 2>&1; then
    export GITHUB_TOKEN="$(gh auth token 2>/dev/null)"
fi
```

`~/.config/zsh/local.zsh` is intentionally **not managed by chezmoi and must never be committed to this repository**.

The configuration model is:

```text
chezmoi-managed config
        |
        └── hosts/work-mac.zsh
                 |
                 └── ~/.config/zsh/local.zsh
                        └── local-only values
```

This keeps the repository reproducible while allowing each machine to have private runtime configuration.

## Git Workflow

Commits use Conventional Commits:

``` text
type(scope): description
```

Examples:

``` text
feat(zsh): add helper
fix(chezmoi): improve bootstrap
docs(readme): update documentation
chore(repo): update metadata
```

## Roadmap

-   Improve bootstrap validation
-   Add automated checks
-   Expand workstation automation
-   Document recovery procedures

## License

Private configuration repository.
