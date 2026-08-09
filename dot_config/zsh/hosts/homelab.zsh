# ============================================================
# Lincoln homelab
# ============================================================

alias dps='docker ps'
alias dcu='docker compose up -d'
alias dcd='docker compose down'
alias dcl='docker compose logs -f'

[[ -d /mnt/storage ]] &&
    alias storage='cd /mnt/storage'

[[ -d /mnt/storage/docker/stacks ]] &&
    alias stacks='cd /mnt/storage/docker/stacks'
