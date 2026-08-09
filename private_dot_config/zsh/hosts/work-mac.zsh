# ============================================================
# Work Mac
# ============================================================

export PATH="/opt/homebrew/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"

[[ -d "/Applications/IntelliJ IDEA.app/Contents/MacOS" ]] &&
    export PATH="/Applications/IntelliJ IDEA.app/Contents/MacOS:$PATH"

[[ -d /opt/homebrew/opt/libpq/bin ]] &&
    export PATH="/opt/homebrew/opt/libpq/bin:$PATH"

# Default JDK: 17
if [[ -d /opt/homebrew/opt/openjdk@17 ]]; then
    export JAVA_HOME="/opt/homebrew/opt/openjdk@17"
    export PATH="$JAVA_HOME/bin:$PATH"
fi

usejdk17() {
    export JAVA_HOME="/opt/homebrew/opt/openjdk@17"
    export PATH="$(echo "$PATH" | tr ':' '\n' | grep -v '/opt/homebrew/opt/openjdk@' | paste -sd ':' -)"
    export PATH="$JAVA_HOME/bin:$PATH"
    java -version
}

usejdk21() {
    export JAVA_HOME="/opt/homebrew/opt/openjdk@21"
    export PATH="$(echo "$PATH" | tr ':' '\n' | grep -v '/opt/homebrew/opt/openjdk@' | paste -sd ':' -)"
    export PATH="$JAVA_HOME/bin:$PATH"
    java -version
}

# SDKMAN
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$SDKMAN_DIR/bin/sdkman-init.sh" ]] && source "$SDKMAN_DIR/bin/sdkman-init.sh"

export NVM_DIR="$HOME/.nvm"
[[ -s "$NVM_DIR/nvm.sh" ]] && source "$NVM_DIR/nvm.sh"
[[ -s "$NVM_DIR/bash_completion" ]] && source "$NVM_DIR/bash_completion"

# Only expose the GitHub token when explicitly requested.
github-token() {
    export AUTH_TOKEN="$(gh auth token)"
    echo "AUTH_TOKEN exported for this shell."
}

github-token-clear() {
    unset AUTH_TOKEN
    echo "AUTH_TOKEN removed from this shell."
}
