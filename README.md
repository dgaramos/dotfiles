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
