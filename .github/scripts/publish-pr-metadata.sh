#!/usr/bin/env bash
# Non-fatal metadata publisher: labels/milestone/assignee first, Project V2 last.
# Each step emits a warning on failure but never aborts the script.
set -uo pipefail

: "${PR_NUMBER:?PR_NUMBER is required}"
: "${BASE_BRANCH:?BASE_BRANCH is required}"
: "${EXPECTED_AUTHOR:?EXPECTED_AUTHOR is required}"
: "${PUBLISHER_APP_SLUG:?PUBLISHER_APP_SLUG is required}"

[[ "$PUBLISHER_APP_SLUG" == "${EXPECTED_AUTHOR%\[bot\]}" ]] || {
  echo "unexpected authenticated app" >&2
  exit 1
}

mapfile -t labels < <(jq -er '.[] | strings | select(length > 0)' <<<"${LABELS_JSON:-[]}")
mapfile -t assignees < <(jq -er '.[] | strings | select(length > 0)' <<<"${ASSIGNEES_JSON:-[]}")

# ── Step 1: labels, milestone, assignee (non-fatal) ──────────────────────────
core_args=(
  --repo "$GITHUB_REPOSITORY"
  --pr "$PR_NUMBER"
  --base "$BASE_BRANCH"
)
for label in "${labels[@]}"; do core_args+=(--label "$label"); done
for assignee in "${assignees[@]}"; do core_args+=(--assignee "$assignee"); done
[[ -z "${MILESTONE_NUMBER:-}" ]] || core_args+=(--milestone "$MILESTONE_NUMBER")

if bash core/issue-workflow/scripts/apply-pr-metadata.sh "${core_args[@]}"; then
  echo "core metadata (labels/milestone/assignee) applied and verified"
else
  echo "WARNING: core metadata step failed; labels/milestone/assignee may be incomplete" >&2
fi

# ── Step 2: Project V2 (non-fatal) ───────────────────────────────────────────
# User-owned projectV2 may be inaccessible to the App token even with
# permission-projects:write, because that permission covers org-scoped projects.
# Attempt the step and emit a clear warning rather than aborting.
if [[ -n "${PROJECT_OWNER:-}${PROJECT_NUMBER:-}${PROJECT_STATUS:-}" ]]; then
  if [[ -z "${PROJECT_OWNER:-}" || -z "${PROJECT_NUMBER:-}" || -z "${PROJECT_STATUS:-}" ]]; then
    echo "WARNING: project owner, number, and status must be supplied together — skipping Project step" >&2
  else
    project_args=(
      --repo "$GITHUB_REPOSITORY"
      --pr "$PR_NUMBER"
      --base "$BASE_BRANCH"
      --project-owner "$PROJECT_OWNER"
      --project-number "$PROJECT_NUMBER"
      --project-status "$PROJECT_STATUS"
    )
    if bash core/issue-workflow/scripts/apply-pr-metadata.sh "${project_args[@]}"; then
      echo "Project V2 step applied and verified"
    else
      echo "WARNING: Project V2 step failed (user-owned projectV2 may be inaccessible to the App token); other metadata was applied successfully" >&2
    fi
  fi
fi
