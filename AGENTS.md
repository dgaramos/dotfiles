# AGENTS.md

## Purpose

Instructions for AI agents working on this repository.

This repository manages personal dotfiles through chezmoi.

## Rules

### Secrets

Never add:

-   tokens
-   passwords
-   credentials
-   private keys
-   secret environment files

### Configuration placement

Use the correct layer:

-   shared -\> `common.zsh`
-   personal Mac -\> `hosts/mac.zsh`
-   work Mac -\> `hosts/work-mac.zsh`
-   homelab -\> `hosts/homelab.zsh`
-   Steam Deck -\> `hosts/steamdeck.zsh`

### Shell

Prefer portable shell code:

``` zsh
if command -v tool >/dev/null 2>&1; then
    tool setup
fi
```

### Chezmoi

After changes:

``` bash
chezmoi diff
chezmoi apply
```

### Commits

Use Conventional Commits:

-   `feat(scope): description`
-   `fix(scope): description`
-   `docs(scope): description`
-   `chore(scope): description`

### Before editing

1.  Identify affected machine.
2.  Choose the correct configuration layer.
3.  Make the smallest safe change.
4.  Validate.

Ask before destructive operations such as history rewrites or major
removals.

## Machines

-   Nautilus-M3-Pro
-   Work Mac
-   lincoln-lab-pi-5
-   Steam Deck
