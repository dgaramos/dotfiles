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

## Publisher dispatch
Both Claudio DR and Cody DR have a publisher installed for every mode below.
Each row names a workflow file present in `.github/workflows/` right now; the
table is a path-for-path record of what is installed, not a list of intended
capability.

| Mode | Claudio DR workflow | Cody DR workflow |
| --- | --- | --- |
| create-issue | `publish-claudio-issue.yml` | `publish-cody-issue.yml` |
| issue-comment | `publish-claudio-issue-comment.yml` | `publish-cody-issue-comment.yml` |
| create-pr | `publish-claudio-pr.yml` | `publish-cody-pr.yml` |
| apply-pr-metadata | `publish-claudio-pr-metadata.yml` | `publish-cody-pr-metadata.yml` |
| reply | `publish-claudio-reply.yml` | `publish-cody-reply.yml` |
| resolve-thread | `publish-claudio-resolve.yml` | `publish-cody-resolve.yml` |
| review | `publish-claudio-review.yml` | `publish-cody-review.yml` |

Reviewer identities are `claudio-dr[bot]`, authenticated through the
`claudio-dr` GitHub App, and `cody-dr[bot]`, authenticated through the `cody-dr`
GitHub App. Dispatch only the publisher matching the acting agent, and only
after explicit user authorization. Verify that the resulting author is that
agent's bot; a failed author verification is a failed publication, not a
fallback trigger. A personal GitHub account may publish only as a disclosed
fallback, and only when the App operation is proven unavailable before dispatch.

Every publication behavior lives in the central `dgaramos/dr-agents` catalog;
the workflow files here are thin dispatch stubs that exist only because
`workflow_dispatch` requires the workflow on the default branch. Fix publisher
behavior in the catalog, never by editing a stub here. Neither `.github/` nor
`.dr-agents/` is managed by chezmoi, so nothing in this section is reachable
through `chezmoi apply`.

## Delivery metadata
This repository imposes no labels, milestone, assignee, or Project values on
issues or pull requests. Use only values explicitly supplied, or inherited from
a linked issue.

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
