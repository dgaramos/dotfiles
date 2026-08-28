#!/usr/bin/env bash
set -euo pipefail

: "${GH_TOKEN:?GH_TOKEN is required}"
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"
: "${PR_NUMBER:?PR_NUMBER is required}"
: "${REVIEW_EVENT:?REVIEW_EVENT is required}"
: "${REVIEWED_HEAD_SHA:?REVIEWED_HEAD_SHA is required}"
: "${EXPECTED_AUTHOR:?EXPECTED_AUTHOR is required}"
: "${PUBLISHER_APP_SLUG:?PUBLISHER_APP_SLUG is required}"

readonly inline_comments_json="${INLINE_COMMENTS_JSON:-[]}"
readonly replies_json="${REPLIES_JSON:-[]}"
readonly resolve_thread_ids_json="${RESOLVE_THREAD_IDS_JSON:-[]}"
[[ "$PR_NUMBER" =~ ^[1-9][0-9]*$ ]] || { echo "pr_number must be a positive integer" >&2; exit 1; }
[[ "$REVIEWED_HEAD_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo "reviewed_head_sha must be a full SHA" >&2; exit 1; }
[[ "$PUBLISHER_APP_SLUG" == "${EXPECTED_AUTHOR%\[bot\]}" ]] || { echo "unexpected authenticated app" >&2; exit 1; }
case "$REVIEW_EVENT" in APPROVE) expected_state=APPROVED ;; COMMENT) expected_state=COMMENTED ;; REQUEST_CHANGES) expected_state=CHANGES_REQUESTED ;; *) echo "unsupported review event" >&2; exit 1 ;; esac
jq -e 'type == "array" and all(.[]; type == "object" and (.path | type == "string" and length > 0) and (.line | type == "number" and floor == . and . > 0) and (.body | type == "string" and length > 0))' <<<"$inline_comments_json" >/dev/null || { echo "invalid inline_comments_json" >&2; exit 1; }
jq -e 'type == "array" and all(.[]; type == "object" and (.comment_id | type == "number" and floor == . and . > 0) and (.body | type == "string" and length > 0))' <<<"$replies_json" >/dev/null || { echo "invalid replies_json" >&2; exit 1; }
jq -e 'type == "array" and all(.[]; type == "string" and length > 0)' <<<"$resolve_thread_ids_json" >/dev/null || { echo "invalid resolve_thread_ids_json" >&2; exit 1; }
readonly expected_pr_url="https://api.github.com/repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}"
[[ "$(gh api "repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}" --jq .head.sha)" == "$REVIEWED_HEAD_SHA" ]] || { echo "PR head changed since review" >&2; exit 1; }
publish_review=false
if [[ -n "${REVIEW_BODY:-}" ]] || [[ "$(jq length <<<"$inline_comments_json")" -gt 0 ]]; then publish_review=true; fi
[[ "$publish_review" == true || "$(jq length <<<"$replies_json")" -gt 0 || "$(jq length <<<"$resolve_thread_ids_json")" -gt 0 ]] || { echo "provide a review body, inline finding, reply, or resolution" >&2; exit 1; }
while IFS= read -r reply; do
  comment_id="$(jq -r '.comment_id' <<<"$reply")"
  [[ "$(gh api "repos/${GITHUB_REPOSITORY}/pulls/comments/${comment_id}" --jq .pull_request_url)" == "$expected_pr_url" ]] || { echo "reply target mismatch" >&2; exit 1; }
  [[ -z "$(gh api "repos/${GITHUB_REPOSITORY}/pulls/comments/${comment_id}" --jq '.in_reply_to_id // empty')" ]] || { echo "reply target must be a top-level review comment" >&2; exit 1; }
done < <(jq -c '.[]' <<<"$replies_json")
while IFS= read -r thread_id; do
  cursor=""; found=false
  while :; do
    args=(-f query='query($owner: String!, $name: String!, $number: Int!, $after: String) { repository(owner: $owner, name: $name) { pullRequest(number: $number) { reviewThreads(first: 100, after: $after) { nodes { id } pageInfo { hasNextPage endCursor } } } } }' -f owner="${GITHUB_REPOSITORY%%/*}" -f name="${GITHUB_REPOSITORY##*/}" -F number="$PR_NUMBER")
    [[ -z "$cursor" ]] || args+=(-f after="$cursor")
    threads="$(gh api graphql "${args[@]}")"
    if jq -e --arg thread "$thread_id" '.data.repository.pullRequest.reviewThreads.nodes | any(.id == $thread)' <<<"$threads" >/dev/null; then found=true; break; fi
    [[ "$(jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.hasNextPage' <<<"$threads")" == true ]] || break
    cursor="$(jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.endCursor' <<<"$threads")"
  done
  [[ "$found" == true ]] || { echo "resolution target mismatch" >&2; exit 1; }
done < <(jq -r '.[]' <<<"$resolve_thread_ids_json")
if [[ "$publish_review" == true ]]; then
  jq -n --arg event "$REVIEW_EVENT" --arg body "${REVIEW_BODY:-}" --arg commit_id "$REVIEWED_HEAD_SHA" --argjson comments "$inline_comments_json" '{event: $event, body: $body, commit_id: $commit_id} + (if ($comments | length) == 0 then {} else {comments: ($comments | map({path, line, side: "RIGHT", body}))} end)' > review.json
  gh api --method POST "repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}/reviews" --input review.json > created-review.json
  [[ "$(jq -r '.user.login' created-review.json)" == "$EXPECTED_AUTHOR" ]] || { echo "unexpected review author" >&2; exit 1; }
  [[ "$(jq -r '.pull_request_url' created-review.json)" == "$expected_pr_url" ]] || { echo "review target mismatch" >&2; exit 1; }
  [[ "$(jq -r '.state' created-review.json)" == "$expected_state" ]] || { echo "unexpected review state" >&2; exit 1; }
fi
while IFS= read -r reply; do
  comment_id="$(jq -r '.comment_id' <<<"$reply")"; reply_body="$(jq -r '.body' <<<"$reply")"
  gh api --method POST "repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}/comments" -f body="$reply_body" -F in_reply_to="$comment_id" > created-reply.json
  [[ "$(jq -r '.user.login' created-reply.json)" == "$EXPECTED_AUTHOR" ]] || { echo "unexpected reply author" >&2; exit 1; }
done < <(jq -c '.[]' <<<"$replies_json")
resolved_count=0
while IFS= read -r thread_id; do
  if resolve_out="$(gh api graphql -f query='mutation($thread: ID!) { resolveReviewThread(input: {threadId: $thread}) { thread { isResolved } } }' -f thread="$thread_id" --jq '.data.resolveReviewThread.thread.isResolved' 2>&1)" && [[ "$resolve_out" == "true" ]]; then
    resolved_count=$((resolved_count + 1))
  else
    echo "warning: could not resolve thread ${thread_id} (skipped): ${resolve_out}" >&2
  fi
done < <(jq -r '.[]' <<<"$resolve_thread_ids_json")
printf 'Publication report: review=%s inline=%s replies=%s resolutions=%s/%s\n' "$publish_review" "$(jq length <<<"$inline_comments_json")" "$(jq length <<<"$replies_json")" "$resolved_count" "$(jq length <<<"$resolve_thread_ids_json")"
