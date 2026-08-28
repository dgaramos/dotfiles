#!/usr/bin/env bash
# Apply and verify PR metadata declared by a target profile.  This helper has
# no repository defaults: callers supply every target-specific value.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: apply-pr-metadata.sh --repo OWNER/REPO --pr NUMBER --base BRANCH [options]

Required options:
  --repo OWNER/REPO       Repository containing the pull request
  --pr NUMBER             Pull request number
  --base BRANCH           Expected base branch

Metadata options (repeat label, assignee, and reviewer as needed):
  --label NAME
  --milestone TITLE
  --assignee LOGIN
  --reviewer LOGIN
  --project-owner LOGIN_OR_ORG --project-number NUMBER --project-status STATUS
EOF
}

repo="" pr="" base="" milestone="" project_owner="" project_number="" project_status=""
labels=() assignees=() reviewers=()
while (($#)); do
  case "$1" in
    --repo) repo="$2"; shift 2 ;;
    --pr) pr="$2"; shift 2 ;;
    --base) base="$2"; shift 2 ;;
    --label) labels+=("$2"); shift 2 ;;
    --milestone) milestone="$2"; shift 2 ;;
    --assignee) assignees+=("$2"); shift 2 ;;
    --reviewer) reviewers+=("$2"); shift 2 ;;
    --project-owner) project_owner="$2"; shift 2 ;;
    --project-number) project_number="$2"; shift 2 ;;
    --project-status) project_status="$2"; shift 2 ;;
    --help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ -n "$repo" && -n "$pr" && -n "$base" ]] || { usage >&2; exit 2; }
if [[ -n "$project_owner$project_number$project_status" ]] && [[ -z "$project_owner" || -z "$project_number" || -z "$project_status" ]]; then
  echo "project owner, number, and status must be supplied together" >&2
  exit 2
fi

pr_ref="$pr"
for label in "${labels[@]}"; do gh pr edit "$pr_ref" --repo "$repo" --add-label "$label"; done
milestone_title="$milestone"
if [[ "$milestone" =~ ^[0-9]+$ ]]; then
  milestone_title="$(gh api "repos/${repo}/milestones/${milestone}" --jq .title)"
fi
[[ -z "$milestone_title" ]] || gh pr edit "$pr_ref" --repo "$repo" --milestone "$milestone_title"
for assignee in "${assignees[@]}"; do gh pr edit "$pr_ref" --repo "$repo" --add-assignee "$assignee"; done
for reviewer in "${reviewers[@]}"; do gh pr edit "$pr_ref" --repo "$repo" --add-reviewer "$reviewer"; done

if [[ -n "$project_owner" ]]; then
  project_json="$(gh project view "$project_number" --owner "$project_owner" --format json)"
  project_id="$(jq -er '.id' <<<"$project_json")"
  item_json="$(gh project item-add "$project_number" --owner "$project_owner" --url "https://github.com/${repo}/pull/${pr}" --format json)"
  item_id="$(jq -er '.id' <<<"$item_json")"
  fields_json="$(gh project field-list "$project_number" --owner "$project_owner" --format json)"
  field_id="$(jq -er '.fields[] | select(.name == "Status") | .id' <<<"$fields_json")"
  option_id="$(jq -er --arg status "$project_status" '.fields[] | select(.name == "Status") | .options[] | select(.name == $status) | .id' <<<"$fields_json")"
  gh project item-edit --id "$item_id" --project-id "$project_id" --field-id "$field_id" --single-select-option-id "$option_id"
fi

observed="$(gh pr view "$pr_ref" --repo "$repo" --json baseRefName,labels,milestone,assignees,reviewRequests,projectItems)"
jq -e --arg base "$base" '.baseRefName == $base' <<<"$observed" >/dev/null || { echo "metadata verification failed: base branch" >&2; exit 1; }
for label in "${labels[@]}"; do jq -e --arg value "$label" 'any(.labels[]; .name == $value)' <<<"$observed" >/dev/null || { echo "metadata verification failed: label $label" >&2; exit 1; }; done
if [[ -n "$milestone_title" ]]; then jq -e --arg value "$milestone_title" '.milestone.title == $value' <<<"$observed" >/dev/null || { echo "metadata verification failed: milestone $milestone_title" >&2; exit 1; }; fi
for assignee in "${assignees[@]}"; do jq -e --arg value "$assignee" 'any(.assignees[]; .login == $value)' <<<"$observed" >/dev/null || { echo "metadata verification failed: assignee $assignee" >&2; exit 1; }; done
for reviewer in "${reviewers[@]}"; do jq -e --arg value "$reviewer" 'any(.reviewRequests[]; .login == $value)' <<<"$observed" >/dev/null || { echo "metadata verification failed: reviewer $reviewer" >&2; exit 1; }; done
if [[ -n "$project_owner" ]]; then
  jq -e --arg title "$(jq -er '.title' <<<"$project_json")" 'any(.projectItems[]; .title == $title)' <<<"$observed" >/dev/null || { echo "metadata verification failed: Project item" >&2; exit 1; }
  gh project item-list "$project_number" --owner "$project_owner" --limit 1000 --format json | jq -e --arg id "$item_id" --arg status "$project_status" 'any(.items[]; .id == $id and .status == $status)' >/dev/null || { echo "metadata verification failed: Project status $project_status" >&2; exit 1; }
fi

echo "metadata verified for ${repo}#${pr_ref}"
