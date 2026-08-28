# Project Profile: dgaramos/dotfiles

## Purpose
Personal dotfiles managed with chezmoi. Goal: portable, reproducible shell
environment across machines. The repo is public — no secrets, ever.

## Language / Stack
- Shell: zsh
- Template engine: chezmoi (Go templates)
- Custom tools: Python (tools/sshm, tools/local-env, tools/localz, tools/check-dotfiles)
- Test runner: pytest

## Conventions
- Commits: Conventional Commits (`type(scope): description`)
- Shared shell behavior: `private_dot_config/zsh/common.zsh`
- Host-specific config: `private_dot_config/zsh/hosts/`
- Machine-local values stay outside chezmoi (never committed)
- New aliases/functions require an inline comment (`# category: what it does`)
- New CLI tools require entries in `private_dot_config/zsh/cmds.txt`
- Custom tool binaries: bump `tools/.version` after changes

## Test gate
`pytest tools/ tests/ -v` — all tests must pass before merging.

## No-go rules
- No secrets, tokens, API keys, or credentials committed
- No host-specific values in shared files
- No aliases referencing commands not managed by this repo
- Do not rename `.chezmoiscripts/` files without preserving numeric order

## Reviewer notes
- PRs touching `tools/` should verify `tools/.version` was bumped
- PRs touching `common.zsh` aliases/functions should verify `cmds.txt` was updated
- PRs touching bootstrap scripts should check idempotency
- `version` at repo root is managed by the release workflow — do not edit manually
- `tools/.version` is a separate chezmoi reinstall trigger, distinct from the release version
