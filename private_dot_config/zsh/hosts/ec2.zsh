# ============================================================
# EC2 (Amazon Linux)
# ============================================================

# AWS CLI completions
if command -v aws_completer >/dev/null 2>&1; then
    complete -C aws_completer aws
fi
