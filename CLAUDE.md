# CLAUDE.md

## Project Overview

This repository contains personal dotfiles managed with chezmoi.

The goal is to maintain a portable, reproducible shell environment across multiple machines while keeping host-specific and machine-local configuration isolated.

The repository is private and must not contain secrets.

## Configuration Boundaries

Shared shell behavior belongs in:

```text
private_dot_config/zsh/common.zsh
```

Profile-specific configuration belongs in:

```text
private_dot_config/zsh/personal.zsh
private_dot_config/zsh/work.zsh
```

Host-specific configuration belongs in:

```text
private_dot_config/zsh/hosts/mac.zsh
private_dot_config/zsh/hosts/work-mac.zsh
private_dot_config/zsh/hosts/homelab.zsh
private_dot_config/zsh/hosts/steamdeck.zsh
```

Do not place host-specific values in shared files.

## Machine-local Configuration

Some configuration must remain local to a single machine and outside chezmoi.

### local-env

Machine-local environment variables are managed through the versioned `local-env` tool.

Source:

```text
dot_local/bin/executable_local-env
```

Installed path:

```text
~/.local/bin/local-env
```

Local runtime state:

```text
~/.config/local-env/env
~/.config/local-env/names
```

`env` contains the currently configured environment variables.

`names` is an internal registry of variables managed by `local-env`. It allows new shells to clear inherited variables before loading the current environment state.

Neither file is managed by chezmoi and neither file may be committed.

The main commands are:

```text
local-env set NAME VALUE
local-env unset NAME
local-env get NAME
local-env list
local-env path
local-env edit
```

### local.zsh

The generic machine-local shell escape hatch is:

```text
~/.config/zsh/local.zsh
```

Use it for local shell behavior that does not belong in `local-env`.

`common.zsh` loads the `local-env` state first and `local.zsh` afterwards, allowing intentional local overrides.

Never add `local.zsh` to chezmoi.

## CLI Tools

CLI tooling is managed through:

```text
.chezmoiscripts/run_onchange_install-cli-tools.sh.tmpl
```

Current tools include:

- fzf
- zoxide
- ripgrep
- fd
- bat
- eza
- direnv
- delta

Platform-specific executable differences are handled in shell configuration where necessary, such as `fdfind` and `batcat` on Debian.

Do not replace standard POSIX commands such as `find` or `grep` with incompatible aliases. Use separate convenience aliases such as `ff` and `rgrep`.

## Secrets

Never commit:

- tokens
- passwords
- API keys
- credentials
- private keys
- secret environment files
- authentication material

Machine-local values must remain outside chezmoi.

Prefer retrieving credentials dynamically from platform credential stores or authenticated CLI tools.

For example, a GitHub token should preferably come from GitHub CLI authentication rather than being stored as a literal token in the repository.

## Git Workflow

Use Conventional Commits.

Format:

```text
type(scope): description
```

Examples:

```text
feat(zsh): add machine-local environment manager
fix(zsh): clear inherited local environment variables
docs(readme): document local environment management
refactor(zsh): simplify machine-local configuration
chore(repo): update agent instructions
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

Commit descriptions should be concise, imperative, and written in English.

## Validation

Before committing:

```bash
git diff
git status
chezmoi diff
```

When shell behavior changes:

```bash
chezmoi apply
```

Then test the affected behavior directly on the target machine.

For `local-env`, validate at minimum:

```bash
local-env set TEST_LOCAL_ENV "hello world"
exec zsh
echo "$TEST_LOCAL_ENV"

local-env unset TEST_LOCAL_ENV
exec zsh
echo "${TEST_LOCAL_ENV:-<unset>}"
```

The expected final value after removal is:

```text
<unset>
```

## Working Principles

- Keep shared behavior portable.
- Keep host-specific behavior isolated.
- Keep machine-local values outside version control.
- Prefer feature detection over platform assumptions.
- Make the smallest safe change.
- Validate both chezmoi source changes and rendered output.
- Do not perform destructive Git operations without explicit approval.
