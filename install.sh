#!/usr/bin/env bash
# install.sh — download one or all custom tools from the latest GitHub Release.
#
# Usage:
#   curl -fsSL https://github.com/dgaramos/dotfiles/releases/latest/download/install.sh | bash
#   curl -fsSL https://github.com/dgaramos/dotfiles/releases/latest/download/install.sh | bash -s -- sshm
#
# No sudo, no system directories, no shell-file mutations.

set -euo pipefail

REPO="dgaramos/dotfiles"
BIN_DIR="${HOME}/.local/bin"
ALL_TOOLS=(sshm local-env localz check-dotfiles)

# ---- helpers ----------------------------------------------------------------

die() { printf 'error: %s\n' "$*" >&2; exit 1; }

resolve_latest_tag() {
    local url="https://api.github.com/repos/${REPO}/releases/latest"
    local tag
    tag=$(curl -fsSL "$url" | grep '"tag_name"' | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')
    [ -n "$tag" ] || die "could not resolve latest release tag from ${url}"
    printf '%s' "$tag"
}

install_tool() {
    local tool="$1" tag="$2"
    local url="https://github.com/${REPO}/releases/download/${tag}/${tool}"
    local dest="${BIN_DIR}/${tool}"
    printf 'downloading %s ...\n' "$tool"
    curl -fsSL "$url" -o "$dest" || die "download failed: ${url}"
    chmod +x "$dest"
    printf 'installed %s (%s) -> %s\n' "$tool" "$tag" "$dest"
}

# ---- main -------------------------------------------------------------------

mkdir -p "$BIN_DIR"

TAG=$(resolve_latest_tag)

if [ "$#" -gt 0 ]; then
    TOOLS=("$@")
else
    TOOLS=("${ALL_TOOLS[@]}")
fi

for tool in "${TOOLS[@]}"; do
    install_tool "$tool" "$TAG"
done

case ":${PATH}:" in
    *":${BIN_DIR}:"*) ;;
    *)
        printf '\nNote: %s is not on PATH. Add the following to your shell profile:\n' "$BIN_DIR"
        printf '  export PATH="%s:$PATH"\n\n' "$BIN_DIR"
        ;;
esac
