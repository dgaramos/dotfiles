# AGENTS.md

## Purpose

Instructions for AI agents working on this repository.

This repository manages personal dotfiles through chezmoi.

## Rules

### Secrets

Never add:

- tokens
- passwords
- credentials
- private keys
- secret environment files
- authentication material

Machine-local values must stay outside the chezmoi source state.

Prefer retrieving credentials dynamically from platform credential stores or authenticated CLI tools instead of storing secret values directly in shell files.

### Configuration placement

Use the correct layer:

- shared behavior -> `private_dot_config/zsh/common.zsh`
- personal profile -> `private_dot_config/zsh/personal.zsh`
- work profile -> `private_dot_config/zsh/work.zsh`
- personal Mac -> `private_dot_config/zsh/hosts/mac.zsh`
- work Mac -> `private_dot_config/zsh/hosts/work-mac.zsh`
- homelab -> `private_dot_config/zsh/hosts/homelab.zsh`
- Steam Deck -> `private_dot_config/zsh/hosts/steamdeck.zsh`
- EC2 (Amazon Linux) -> `private_dot_config/zsh/hosts/ec2.zsh`

Do not place host-specific values in shared files.

### Machine-local configuration

Machine-local configuration is intentionally kept outside chezmoi.

Use:

```text
~/.config/local-env/env
```

for machine-local environment variables managed through `local-env`.

The internal registry used by `local-env` is:

```text
~/.config/local-env/names
```

Both files are local runtime state and must never be added to chezmoi or committed.

Use:

```text
~/.config/zsh/local.zsh
```

as a generic machine-local shell escape hatch for configuration that does not belong in `local-env`.

`common.zsh` loads both mechanisms when present.

### local-env

The `local-env` tool is versioned in:

```text
dot_local/bin/executable_local-env
```

and installed as:

```text
~/.local/bin/local-env
```

Use `local-env` for machine-local environment variables instead of adding values directly to chezmoi-managed files.

Supported commands include:

```text
local-env set NAME VALUE
local-env unset NAME
local-env get NAME
local-env list
local-env path
local-env edit
```

The tool itself is managed by chezmoi. The values it manages are not.

### Shell

Prefer portable shell code and feature detection:

```zsh
if command -v tool >/dev/null 2>&1; then
    tool setup
fi
```

Do not replace POSIX commands such as `find` or `grep` with incompatible aliases such as `fd` or `rg`. External scripts and SDKs may depend on standard command behavior.

Use separate convenience aliases instead.

### Chezmoi

Before applying changes:

```bash
chezmoi diff
```

When appropriate:

```bash
chezmoi apply
```

After changes, validate both source state and rendered state.

### Commits

Use Conventional Commits:

```text
type(scope): description
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

Use concise English imperative descriptions.

### Validation

Before committing:

```bash
git diff
git status
chezmoi diff
```

When shell behavior changed, apply and test it on the affected machine before committing.

### Before editing

1. Identify the affected machine or configuration layer.
2. Choose the smallest correct scope.
3. Keep machine-local values outside chezmoi.
4. Make the smallest safe change.
5. Validate rendered chezmoi output.
6. Test shell behavior when relevant.

Ask before destructive operations such as history rewrites, forced pushes, or major removals.

## Machines

- Nautilus-M3-Pro
- Work Mac
- lincoln-lab-pi-5
- Steam Deck
- EC2 (at-open-webui-dedicated, Amazon Linux, Graviton3)
