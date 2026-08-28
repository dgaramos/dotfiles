#!/usr/bin/env bash
set -euo pipefail

: "${GH_TOKEN:?GH_TOKEN is required}"
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"
: "${PR_NUMBER:?PR_NUMBER is required}"
: "${THREAD_ID:?THREAD_ID is required}"
: "${THREAD_ACTION:?THREAD_ACTION is required}"
: "${EXPECTED_AUTHOR:?EXPECTED_AUTHOR is required}"
: "${PUBLISHER_APP_SLUG:?PUBLISHER_APP_SLUG is required}"

[[ "$PR_NUMBER" =~ ^[1-9][0-9]*$ ]] || { echo "pr_number must be a positive integer" >&2; exit 1; }
[[ -n "$THREAD_ID" ]] || { echo "thread_id is required" >&2; exit 1; }
[[ "$PUBLISHER_APP_SLUG" == "${EXPECTED_AUTHOR%\[bot\]}" ]] || { echo "unexpected authenticated app" >&2; exit 1; }
case "$THREAD_ACTION" in
  reply) : "${BODY:?body is required}" ;;
  resolve) ;;
  *) echo "unsupported thread action" >&2; exit 1 ;;
esac

readonly expected_repository="$GITHUB_REPOSITORY"
found=false
cursor=""
while :; do
  args=(-f query='query($owner: String!, $name: String!, $number: Int!, $after: String) { repository(owner: $owner, name: $name) { pullRequest(number: $number) { reviewThreads(first: 100, after: $after) { nodes { id } pageInfo { hasNextPage endCursor } } } } }' -f owner="${GITHUB_REPOSITORY%%/*}" -f name="${GITHUB_REPOSITORY##*/}" -F number="$PR_NUMBER")
  [[ -z "$cursor" ]] || args+=(-f after="$cursor")
  threads="$(gh api graphql "${args[@]}")"
  if jq -e --arg thread "$THREAD_ID" '.data.repository.pullRequest.reviewThreads.nodes | any(.id == $thread)' <<<"$threads" >/dev/null; then found=true; break; fi
  [[ "$(jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.hasNextPage' <<<"$threads")" == true ]] || break
  cursor="$(jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.endCursor' <<<"$threads")"
done
[[ "$found" == true ]] || { echo "thread target mismatch" >&2; exit 1; }

if [[ "$THREAD_ACTION" == reply ]]; then
  result="$(gh api graphql -f query='mutation($thread: ID!, $body: String!) { addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $thread, body: $body}) { comment { author { login } pullRequest { number repository { nameWithOwner } } } } }' -f thread="$THREAD_ID" -f body="$BODY")"
  [[ "$(jq -r '.data.addPullRequestReviewThreadReply.comment.author.login' <<<"$result")" == "$EXPECTED_AUTHOR" ]] || { echo "unexpected reply author" >&2; exit 1; }
  [[ "$(jq -r '.data.addPullRequestReviewThreadReply.comment.pullRequest.number' <<<"$result")" == "$PR_NUMBER" ]] || { echo "reply target mismatch" >&2; exit 1; }
  [[ "$(jq -r '.data.addPullRequestReviewThreadReply.comment.pullRequest.repository.nameWithOwner' <<<"$result")" == "$expected_repository" ]] || { echo "reply repository mismatch" >&2; exit 1; }
else
  gh api graphql -f query='mutation($thread: ID!) { resolveReviewThread(input: {threadId: $thread}) { thread { isResolved } } }' -f thread="$THREAD_ID" --jq '.data.resolveReviewThread.thread.isResolved' | grep -qx true
fi

printf 'Publication report: action=%s pr=%s thread=%s\n' "$THREAD_ACTION" "$PR_NUMBER" "$THREAD_ID"
