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

## Bootstrap Scripts

Scripts in `.chezmoiscripts/` run automatically during `chezmoi apply`. Execution order is enforced by numeric prefixes — never rename without preserving the order.

```text
run_once_01-install-zsh          → installs zsh + sets as default shell (Linux only)
run_once_02-install-homebrew     → installs Homebrew (macOS only)
run_once_03-install-oh-my-zsh    → installs oh-my-zsh
run_once_04-install-zsh-plugins  → clones zsh plugins
run_onchange_install-cli-tools   → installs CLI tools (re-runs when content changes)
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

## Secret Scanner (check-dotfiles)

The repository includes a `check-dotfiles` scanner installed as a pre-commit hook.

Source:

```text
dot_local/bin/executable_check-dotfiles
```

Installed path:

```text
~/.local/bin/check-dotfiles
```

The hook runs automatically on every commit. It can also be run manually:

```text
check-dotfiles --staged   → scan staged files
check-dotfiles --all      → scan all tracked files
```

It blocks commits containing secrets, private IPs, EC2 hostnames, and aliases referencing external services not installed by this repository. Add `# check-dotfiles: ignore` to suppress false positives.

## Local Shell Manager (localz)

The repository includes a `localz` utility for managing `~/.config/zsh/local.zsh`.

Source:

```text
dot_local/bin/executable_localz
```

Installed path:

```text
~/.local/bin/localz
```

The main commands are:

```text
localz edit           → open local.zsh in $EDITOR
localz show           → print local.zsh contents
localz list           → list aliases and functions defined in local.zsh
localz add NAME CMD   → append an alias to local.zsh
```

## SSH Manager (sshm)

The repository includes an `sshm` utility for managing SSH connections.

Source:

```text
dot_local/bin/executable_sshm
```

Installed path:

```text
~/.local/bin/sshm
```

The main commands are:

```text
sshm list                  → show configured SSH hosts (HOST, HOSTNAME, USER, KEY)
sshm add                   → interactive wizard to add a new SSH host
sshm edit                  → open ~/.ssh/config in $EDITOR
sshm copy-id <host>        → install a public key on a remote host
sshm keygen                → generate a new key pair
```

`sshm add` handles `.pem` files by copying them to `~/.ssh/`, setting permissions to 400, deriving the public key, and writing the appropriate `~/.ssh/config` block.

`sshm copy-id` accepts `.pem` keys by deriving the public key with `ssh-keygen -y -f`.

Infrastructure-specific SSH aliases (IPs, host names for private servers) must never be committed. Configure them via `sshm add` and keep them in `~/.ssh/config` locally.

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
