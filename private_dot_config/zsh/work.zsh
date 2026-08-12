# ============================================================
# Work profile
# ============================================================

# Intentionally contains no personal credentials or infrastructure secrets.

if command -v gh >/dev/null 2>&1; then
    alias prs='gh pr list'
    alias mypr='gh pr list --author=@me'
    alias prv='gh pr view --web'
    alias issues='gh issue list'
fi
