# CLAUDE.md

## Project Overview

This repository contains personal dotfiles managed with chezmoi.

The goal is to maintain a portable, reproducible shell environment across multiple machines while keeping host-specific and machine-local configuration isolated.

The repository is public. It must not contain secrets.

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
private_dot_config/zsh/hosts/ec2.zsh
```

Do not place host-specific values in shared files.

## Machine-local Configuration

Some configuration must remain local to a single machine and outside chezmoi.

### local-env

Machine-local environment variables are managed through the `local-env` tool.

See `tools/local-env/CLAUDE.md` for implementation details.

Local runtime state (never managed by chezmoi):

```text
~/.config/local-env/env
~/.config/local-env/names
```

### local.zsh

The generic machine-local shell escape hatch is:

```text
~/.config/zsh/local.zsh
```

Use it for local shell behavior that does not belong in `local-env`.

`common.zsh` loads the `local-env` state first and `local.zsh` afterwards, allowing intentional local overrides.

Never add `local.zsh` to chezmoi.

## Custom Tools

Custom CLI utilities live in `tools/`. Each tool has its own `README.md`, `CLAUDE.md`, and `AGENTS.md` — read those before editing a tool.

| Tool | Source | Installed |
|---|---|---|
| `sshm` | `tools/sshm/` | `~/.local/bin/sshm` |
| `local-env` | `tools/local-env/` | `~/.local/bin/local-env` |
| `localz` | `tools/localz/` | `~/.local/bin/localz` |
| `check-dotfiles` | `tools/check-dotfiles/` | `~/.local/bin/check-dotfiles` |

Installation is handled by `run_onchange_install-tools.sh.tmpl`. The `tools/` directory is in `.chezmoiignore`. Bump `tools/.version` after changing any tool binary so the install script re-runs on all machines.

### Interactive selection menus

Any Python CLI that presents a list of options must use `select_interactive` — never numbered prompts. See `tools/sshm/CLAUDE.md` for the canonical implementation.

## Bootstrap Scripts

Scripts in `.chezmoiscripts/` run automatically during `chezmoi apply`. Execution order is enforced by numeric prefixes — never rename without preserving the order.

```text
run_once_01-install-zsh          → installs zsh + sets as default shell (Linux only)
run_once_02-install-homebrew     → installs Homebrew (macOS only)
run_once_03-install-oh-my-zsh    → installs oh-my-zsh
run_once_04-install-zsh-plugins  → clones zsh plugins
run_onchange_install-cli-tools   → installs CLI tools (re-runs when content changes)
run_onchange_install-tools       → installs custom tools from tools/ (re-runs on version bump)
```

`run_once_` scripts are tracked by filename. Renaming causes them to re-run on all machines — acceptable only when scripts are idempotent.

`run_onchange_` scripts re-run whenever the file content changes, on all machines.

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
- starship
- gh

Platform-specific executable differences are handled in shell configuration where necessary, such as `fdfind` and `batcat` on Debian.

On apt and dnf systems, `starship` is installed via its official installer since it is not available as a standard distribution package.

`gh` is only installed on macOS by these dotfiles. Linux machines may have it installed separately.

Do not replace standard POSIX commands such as `find` or `grep` with incompatible aliases. Use separate convenience aliases such as `ff` and `rgrep`.

Aliases must only reference commands that this repository installs or that are standard system commands available on all supported platforms. Never alias commands for external services or applications not managed here (e.g. `open-webui`, `nginx`, application-specific CLIs). Those belong in `~/.config/zsh/local.zsh` on the specific machine.

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
