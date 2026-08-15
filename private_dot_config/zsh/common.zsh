# ============================================================
# Shared shell configuration
# ============================================================

export PATH="$HOME/.local/bin:$PATH"

# History
HISTFILE="$HOME/.zsh_history"
HISTSIZE=100000
SAVEHIST=100000

setopt EXTENDED_HISTORY
setopt HIST_IGNORE_DUPS
setopt HIST_FIND_NO_DUPS
setopt HIST_REDUCE_BLANKS
setopt SHARE_HISTORY
setopt INC_APPEND_HISTORY

# Navigation
alias c='clear'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# Git
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'
alias gd='git diff'
alias gb='git branch'
alias gco='git checkout'

# GitHub CLI
if command -v gh >/dev/null 2>&1; then
    alias prs='gh pr list'
    alias mypr='gh pr list --author=@me'
    alias prv='gh pr view'
    alias issues='gh issue list'
fi

# Chezmoi
alias cz='chezmoi'
alias czd='chezmoi diff'
alias cza='chezmoi apply'
alias czu='chezmoi update'
alias cze='chezmoi edit'
alias zshr='exec zsh'

if command -v starship >/dev/null 2>&1; then
    eval "$(starship init zsh)"
fi

# ============================================================
# Optional modern CLI tools
# ============================================================

if command -v eza >/dev/null 2>&1; then
    alias ls='eza'
    alias ll='eza -lah --icons'
    alias la='eza -la --icons'
    alias tree='eza --tree --icons'
fi

if command -v bat >/dev/null 2>&1; then
    alias cat='bat'
elif command -v batcat >/dev/null 2>&1; then
    alias cat='batcat'
fi

if command -v rg >/dev/null 2>&1; then
    alias rgrep='rg'
fi

if command -v fd >/dev/null 2>&1; then
    alias ff='fd'
elif command -v fdfind >/dev/null 2>&1; then
    alias ff='fdfind'
fi

# FZF
if command -v fzf >/dev/null 2>&1; then
    if command -v brew >/dev/null 2>&1; then
        FZF_PREFIX="$(brew --prefix fzf)"
    fi

    if [[ -n "$FZF_PREFIX" ]]; then
        [[ -f "$FZF_PREFIX/shell/completion.zsh" ]] && \
            source "$FZF_PREFIX/shell/completion.zsh"

        [[ -f "$FZF_PREFIX/shell/key-bindings.zsh" ]] && \
            source "$FZF_PREFIX/shell/key-bindings.zsh"
    fi

    export FZF_DEFAULT_OPTS="
    --height 40%
    --layout=reverse
    --border
    "
fi


# FZF powered by fd
if command -v fzf >/dev/null 2>&1; then
    if command -v fd >/dev/null 2>&1; then
        FZF_FD_COMMAND="fd"
    elif command -v fdfind >/dev/null 2>&1; then
        FZF_FD_COMMAND="fdfind"
    fi

    if [[ -n "${FZF_FD_COMMAND:-}" ]]; then
        export FZF_DEFAULT_COMMAND="$FZF_FD_COMMAND --hidden --strip-cwd-prefix --exclude .git"
        export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
        export FZF_ALT_C_COMMAND="$FZF_FD_COMMAND --type d --hidden --exclude .git"

        export FZF_CTRL_T_OPTS="
        --preview 'bat --color=always --line-range :200 {} 2>/dev/null || ls {}'
        "

        export FZF_ALT_C_OPTS="
        --preview 'eza --tree --level=2 {} 2>/dev/null'
        "
    fi
fi

# Execution time report: start timestamp, end timestamp, delta
preexec() {
    _cmd_start=$EPOCHSECONDS
    echo "\033[2m▶ $(date '+%H:%M:%S')\033[0m"
}

precmd() {
    if [[ -n $_cmd_start ]]; then
        local delta=$(( EPOCHSECONDS - _cmd_start ))
        local end_time=$(date '+%H:%M:%S')

        if (( delta >= 3600 )); then
            local duration="$(( delta / 3600 ))h $(( (delta % 3600) / 60 ))m $(( delta % 60 ))s"
        elif (( delta >= 60 )); then
            local duration="$(( delta / 60 ))m $(( delta % 60 ))s"
        else
            local duration="${delta}s"
        fi

        echo "\033[2m■ $end_time (+${duration})\033[0m"
        unset _cmd_start
    fi
}

# History substring search
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down

# zoxide
if command -v zoxide >/dev/null 2>&1; then
    eval "$(zoxide init zsh)"
fi

# Direnv
if command -v direnv >/dev/null 2>&1; then
    eval "$(direnv hook zsh)"
fi

# tmux
if command -v tmux >/dev/null 2>&1; then
    # attach to named session or create it (default: main)
    tm() { tmux new-session -A -s "${1:-main}" }
    alias tls='tmux ls'
    alias tks='tmux kill-session -t'
    alias td='tmux detach'
fi

# Machine-local environment variables managed by local-env.
# Clear previously managed variables first so removed values are not
# inherited by a new shell.
if [[ -f "$HOME/.config/local-env/names" ]]; then
    while IFS= read -r name; do
        [[ -n "$name" ]] && unset "$name"
    done < "$HOME/.config/local-env/names"
fi

if [[ -f "$HOME/.config/local-env/env" ]]; then
    source "$HOME/.config/local-env/env"
fi

# Machine-local configuration.
# This file is intentionally not managed by chezmoi.
if [[ -f "$HOME/.config/zsh/local.zsh" ]]; then
    source "$HOME/.config/zsh/local.zsh"
fi
