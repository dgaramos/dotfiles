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
    alias ll='eza -lah'
    alias la='eza -la'
    alias tree='eza --tree'
fi

if command -v bat >/dev/null 2>&1; then
    alias cat='bat'
fi

# FZF
[[ -f "$HOME/.fzf.zsh" ]] && source "$HOME/.fzf.zsh"

# History substring search
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down
