# ============================================================
# Shared shell configuration
# ============================================================

export PATH="$HOME/.local/bin:$PATH"

# History
HISTFILE="$HOME/.zsh_history"
HISTSIZE=100000
SAVEHIST=100000

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

# Chezmoi
alias cz='chezmoi'
alias czd='chezmoi diff'
alias cza='chezmoi apply'
alias czu='chezmoi update'
alias cze='chezmoi edit'

# Always make it obvious which machine this shell belongs to.
PROMPT='%{$fg_bold[green]%}➜  %{$fg[cyan]%}%n@%m %{$fg[blue]%}%~%{$reset_color%} $(git_prompt_info)'

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

# Git delta
if command -v delta >/dev/null 2>&1; then
    git config --global core.pager delta
    git config --global interactive.diffFilter 'delta --color-only'
    git config --global delta.navigate true
    git config --global delta.side-by-side true
fi

# Machine-local configuration.
# This file is intentionally not managed by chezmoi.
if [[ -f "$HOME/.config/zsh/local.zsh" ]]; then
    source "$HOME/.config/zsh/local.zsh"
fi
