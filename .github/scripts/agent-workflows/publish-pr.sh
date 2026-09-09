#!/usr/bin/env bash
set -euo pipefail

: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"
: "${TITLE:?TITLE is required}"
: "${BODY:?BODY is required}"
: "${HEAD_BRANCH:?HEAD_BRANCH is required}"
: "${BASE_BRANCH:?BASE_BRANCH is required}"
: "${EXPECTED_AUTHOR:?EXPECTED_AUTHOR is required}"
: "${PUBLISHER_APP_SLUG:?PUBLISHER_APP_SLUG is required}"
[[ "$PUBLISHER_APP_SLUG" == "${EXPECTED_AUTHOR%\[bot\]}" ]] || { echo "unexpected authenticated app" >&2; exit 1; }
[[ "$HEAD_BRANCH" != "$BASE_BRANCH" ]] || { echo "head and base must differ" >&2; exit 1; }
existing="$(gh api --method GET "repos/${GITHUB_REPOSITORY}/pulls" -f state=open -f "head=${GITHUB_REPOSITORY%%/*}:${HEAD_BRANCH}" -f "base=${BASE_BRANCH}")"
count="$(jq length <<<"$existing")"
if [[ "$count" == 0 ]]; then
  result="$(jq -n --arg title "$TITLE" --arg body "$BODY" --arg head "$HEAD_BRANCH" --arg base "$BASE_BRANCH" \
    '{title:$title, body:$body, head:$head, base:$base}' | gh api --method POST "repos/${GITHUB_REPOSITORY}/pulls" --input -)"
elif [[ "$count" == 1 ]]; then
  result="$(jq '.[0]' <<<"$existing")"
else
  echo "ambiguous existing pull request" >&2
  exit 1
fi
jq -e --arg actor "$EXPECTED_AUTHOR" --arg repo "$GITHUB_REPOSITORY" --arg head "$HEAD_BRANCH" --arg base "$BASE_BRANCH" \
  '.user.login == $actor and .head.ref == $head and .base.ref == $base and .base.repo.full_name == $repo and .head.repo.full_name == $repo' <<<"$result" >/dev/null || { echo "PR actor or target verification failed" >&2; exit 1; }
number="$(jq -er .number <<<"$result")"
observed="$(gh api "repos/${GITHUB_REPOSITORY}/pulls/${number}")"
jq -e --arg actor "$EXPECTED_AUTHOR" --arg title "$TITLE" --arg body "$BODY" --arg head "$HEAD_BRANCH" --arg base "$BASE_BRANCH" \
  '.user.login == $actor and .title == $title and .body == $body and .head.ref == $head and .base.ref == $base' <<<"$observed" >/dev/null || { echo "PR verification failed; inspect the existing PR before retrying" >&2; exit 1; }
jq -r '"Created and verified PR #\(.number): \(.html_url)"' <<<"$observed"
