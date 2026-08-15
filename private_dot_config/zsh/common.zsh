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
alias c='clear'                # clear the terminal
alias ..='cd ..'               # go up one directory
alias ...='cd ../..'           # go up two directories
alias ....='cd ../../..'       # go up three directories

# Git
alias gs='git status'          # show working tree status
alias ga='git add'             # stage files
alias gc='git commit'          # create a commit
alias gp='git push'            # push to remote
alias gl='git pull'            # pull from remote
alias gd='git diff'            # show unstaged changes
alias gb='git branch'          # list or create branches
alias gco='git checkout'       # switch branch or restore files

# GitHub CLI
if command -v gh >/dev/null 2>&1; then
    alias prs='gh pr list'             # list open PRs
    alias mypr='gh pr list --author=@me'  # list my open PRs
    alias prv='gh pr view'             # view a PR
    alias issues='gh issue list'       # list open issues
fi

# Chezmoi
alias cz='chezmoi'             # chezmoi root command
alias czd='chezmoi diff'       # show pending changes
alias cza='chezmoi apply'      # apply dotfiles to home
alias czu='chezmoi update'     # pull + apply from remote
alias cze='chezmoi edit'       # edit a managed file
alias zshr='exec zsh'          # reload zsh shell

if command -v starship >/dev/null 2>&1; then
    eval "$(starship init zsh)"
fi

# ============================================================
# Optional modern CLI tools
# ============================================================

if command -v eza >/dev/null 2>&1; then
    alias ls='eza'                      # list files
    alias ll='eza -lah --icons'         # long list with hidden files
    alias la='eza -la --icons'          # long list
    alias tree='eza --tree --icons'     # directory tree
fi

if command -v bat >/dev/null 2>&1; then
    alias cat='bat'                     # pager with syntax highlight
elif command -v batcat >/dev/null 2>&1; then
    alias cat='batcat'                  # pager with syntax highlight (Debian)
fi

if command -v rg >/dev/null 2>&1; then
    alias rgrep='rg'                    # fast recursive grep
fi

if command -v fd >/dev/null 2>&1; then
    alias ff='fd'                       # fast file finder
elif command -v fdfind >/dev/null 2>&1; then
    alias ff='fdfind'                   # fast file finder (Debian)
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
    tm() { tmux new-session -A -s "${1:-main}" }  # attach or create session (default: main)
    alias tls='tmux ls'              # list sessions
    alias tks='tmux kill-session -t' # kill named session
    alias td='tmux detach'           # detach from current session
fi

# aliases [keyword] — list dotfile aliases and functions, optionally filtered by keyword
aliases() {
    local files=(
        "$HOME/.config/zsh/common.zsh"
        "$HOME/.config/zsh/local.zsh"
    )
    local lines
    lines=$(grep -h -E "^\s*(alias |[a-zA-Z_][a-zA-Z0-9_]*\(\))" "${files[@]}" 2>/dev/null)
    if [[ -n "$1" ]]; then
        echo "$lines" | grep "$1"
    elif command -v fzf >/dev/null 2>&1; then
        echo "$lines" | fzf --height=40% --layout=reverse
    else
        echo "$lines"
    fi
}

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
