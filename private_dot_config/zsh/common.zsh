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
alias c='clear'                # nav: clear the terminal
alias ..='cd ..'               # nav: go up one directory
alias ...='cd ../..'           # nav: go up two directories
alias ....='cd ../../..'       # nav: go up three directories

# Git
alias gs='git status'          # git: show working tree status
alias ga='git add'             # git: stage files
alias gc='git commit'          # git: create a commit
alias gp='git push'            # git: push to remote
alias gl='git pull'            # git: pull from remote
alias gd='git diff'            # git: show unstaged changes
alias gb='git branch'          # git: list or create branches
alias gco='git checkout'       # git: switch branch or restore files

# GitHub CLI
if command -v gh >/dev/null 2>&1; then
    alias prs='gh pr list'             # gh: list open PRs
    alias mypr='gh pr list --author=@me'  # gh: list my open PRs
    alias prv='gh pr view'             # gh: view a PR
    alias issues='gh issue list'       # gh: list open issues
fi

# Chezmoi
alias cz='chezmoi'             # chezmoi: root command
alias czd='chezmoi diff'       # chezmoi: show pending changes
alias cza='chezmoi apply'      # chezmoi: apply dotfiles to home
alias czu='chezmoi update'     # chezmoi: pull + apply from remote
alias cze='chezmoi edit'       # chezmoi: edit a managed file
alias zshr='exec zsh'          # shell: reload zsh

if command -v starship >/dev/null 2>&1; then
    eval "$(starship init zsh)"
fi

# ============================================================
# Optional modern CLI tools
# ============================================================

if command -v eza >/dev/null 2>&1; then
    alias ls='eza'                      # eza: list files
    alias ll='eza -lah --icons'         # eza: long list with hidden files
    alias la='eza -la --icons'          # eza: long list
    alias tree='eza --tree --icons'     # eza: directory tree
fi

if command -v bat >/dev/null 2>&1; then
    alias cat='bat'                     # bat: pager with syntax highlight
elif command -v batcat >/dev/null 2>&1; then
    alias cat='batcat'                  # bat: pager with syntax highlight (Debian)
fi

if command -v rg >/dev/null 2>&1; then
    alias rgrep='rg'                    # rg: fast recursive grep
fi

if command -v fd >/dev/null 2>&1; then
    alias ff='fd'                       # fd: fast file finder
elif command -v fdfind >/dev/null 2>&1; then
    alias ff='fdfind'                   # fd: fast file finder (Debian)
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
    tm() {  # tmux: attach or create session (default: main)
        tmux new-session -A -s "${1:-main}"
    }
    alias tls='tmux ls'              # tmux: list sessions
    alias tks='tmux kill-session -t' # tmux: kill named session
    alias td='tmux detach'           # tmux: detach from current session
fi

# dotcmds [apps|keyword] — browse dotfile aliases, functions and app commands
dotcmds() {  # shell: list aliases, functions and app commands; "apps" for app-only view
    local zsh_files=(
        "$HOME/.config/zsh/common.zsh"
        "$HOME/.config/zsh/local.zsh"
    )
    local cmds_file="$HOME/.config/zsh/cmds.txt"

    local shell_raw app_raw
    shell_raw=$(grep -h -E "^\s*(alias |[a-zA-Z_][a-zA-Z0-9_]*\(\)).*#" "${zsh_files[@]}" 2>/dev/null)
    app_raw=$(grep -E "^\S.*#" "$cmds_file" 2>/dev/null)

    local shell_fmt app_fmt
    shell_fmt=$(echo "$shell_raw" | while IFS= read -r _line; do
        if [[ "$_line" =~ '^[[:space:]]*alias ([^=]+)=.*# (.+)$' ]]; then
            printf "  \033[1;36m%-16s\033[0m %s\n" "${match[1]}" "${match[2]}"
        elif [[ "$_line" =~ '^[[:space:]]*([a-zA-Z_][a-zA-Z0-9_]*)\(\).*# (.+)$' ]]; then
            printf "  \033[1;36m%-16s\033[0m %s\n" "${match[1]}()" "${match[2]}"
        fi
    done)
    app_fmt=$(echo "$app_raw" | while IFS= read -r _line; do
        if [[ "$_line" =~ '^([^#]+[^[:space:]#])[[:space:]]+# (.+)$' ]]; then
            printf "  \033[1;33m%-16s\033[0m %s\n" "${match[1]}" "${match[2]}"
        fi
    done)

    local output
    if [[ "$1" == "apps" ]]; then
        output="$app_fmt"
    elif [[ -n "$1" ]]; then
        output=$(printf "%s\n%s" "$shell_fmt" "$app_fmt" | grep "$1")
    else
        output=$(printf "%s\n%s" "$shell_fmt" "$app_fmt")
    fi

    if command -v fzf >/dev/null 2>&1 && [[ -z "$1" ]]; then
        echo "$output" | fzf --ansi --height=40% --layout=reverse
    else
        echo "$output"
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
