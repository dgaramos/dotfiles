# CLAUDE.md

## Project Overview

This repository contains personal dotfiles managed with chezmoi.

The goal is to maintain a portable, reproducible shell environment
across multiple machines while keeping host-specific configuration
isolated.

The repository is private and must not contain secrets.

## Configuration Boundaries

Shared shell behavior belongs in `private_dot_config/zsh/common.zsh`.

Host-specific configuration belongs in:

-   `hosts/mac.zsh`
-   `hosts/work-mac.zsh`
-   `hosts/homelab.zsh`
-   `hosts/steamdeck.zsh`

Do not place machine-specific settings in shared files.

## CLI Tools

Managed through:

`.chezmoiscripts/run_onchange_install-cli-tools.sh.tmpl`

Current tools:

-   fzf
-   zoxide
-   ripgrep
-   fd
-   bat
-   eza
-   direnv
-   delta

## Secrets

Never commit:

-   tokens
-   passwords
-   API keys
-   private keys
-   secret environment files

Credentials must be retrieved dynamically.

## Git Workflow

Starting with the next commit, use Conventional Commits.

Format:

`type(scope): description`

Examples:

-   `feat(zsh): add claude code alias`
-   `fix(chezmoi): improve portability`
-   `docs(readme): update documentation`
-   `chore(repo): add agent instructions`

Allowed types:

-   feat
-   fix
-   docs
-   refactor
-   chore
-   test
-   build
-   ci

## Validation

Before committing:

``` bash
git diff
git status
chezmoi diff
```

Keep commits small and focused.
