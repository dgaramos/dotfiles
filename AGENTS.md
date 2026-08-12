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

Aliases in chezmoi-managed zsh files must only reference:
- commands installed by this repository (fzf, zoxide, rg, fd, bat, eza, direnv, delta, starship, gh, chezmoi, local-env, sshm)
- standard POSIX/system commands available on all supported platforms

Never alias external services or application-specific commands (e.g. `open-webui`, `nginx`, app-specific CLIs) in the repo. Those belong in `~/.config/zsh/local.zsh` on the specific machine. The `check-dotfiles` scanner enforces this automatically.

### localz

The `localz` utility manages `~/.config/zsh/local.zsh`.

Source: `dot_local/bin/executable_localz`
Installed: `~/.local/bin/localz`

```text
localz edit        → open local.zsh in $EDITOR
localz show        → print local.zsh contents
localz list        → list aliases and functions
localz add NAME CMD → append an alias
```

### check-dotfiles

The `check-dotfiles` scanner runs as a pre-commit hook and can also be run manually.

Source: `dot_local/bin/executable_check-dotfiles`
Installed: `~/.local/bin/check-dotfiles`

```text
check-dotfiles --staged   → scan staged files (used by pre-commit hook)
check-dotfiles --all      → scan all tracked files
check-dotfiles FILE       → scan specific file
```

**Blocks:** private keys, AWS keys, GitHub tokens, secret assignments, EC2 hostnames, aliases referencing known external services (open-webui, nginx, etc.).

**Warns:** IPv4 addresses, aliases referencing commands not installed by this repository.

To suppress a false positive, add `# check-dotfiles: ignore` to the line.

When adding a new tool to the repo, add it to `REPO_INSTALLED` in the script.

### sshm

The `sshm` utility manages SSH host configuration.

Source: `dot_local/bin/executable_sshm`
Installed: `~/.local/bin/sshm`

`sshm list` shows configured hosts with their identity files.
`sshm add` runs an interactive wizard — handles `.pem` files automatically.
`sshm copy-id <host>` installs a public key and supports `.pem` derivation.

Infrastructure-specific SSH host entries (server IPs, private hostnames) must never be committed to this repository. They live in `~/.ssh/config` on each machine.

### Bootstrap scripts

Scripts in `.chezmoiscripts/` run in alphabetical order. Numeric prefixes enforce the correct sequence — do not rename without preserving order:

```text
run_once_01-install-zsh          → Linux only: installs zsh, sets as default shell
run_once_02-install-homebrew     → macOS only: installs Homebrew
run_once_03-install-oh-my-zsh    → installs oh-my-zsh (requires zsh)
run_once_04-install-zsh-plugins  → clones zsh plugins (requires oh-my-zsh)
run_onchange_install-cli-tools   → installs CLI tools via platform package manager
run_onchange_05-configure-gh-auth → authenticates gh if available (any platform)
run_onchange_06-configure-git    → macOS only: sets git identity and wires delta config
run_onchange_install-git-hooks   → installs pre-commit hook in chezmoi source repo
```

`run_onchange_06-configure-git` prompts for `GIT_NAME` and `GIT_EMAIL` on first run if not set via `local-env`, then saves them. On subsequent runs the variables are already loaded by `common.zsh` and no prompt appears.

`run_once_` scripts are tracked by filename — renaming causes a re-run on all machines. Only rename when the script is idempotent.

`run_onchange_` scripts re-run on all machines whenever the file content changes.

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
