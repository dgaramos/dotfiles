# ============================================================
# Personal Mac
# ============================================================

if [[ -d /opt/homebrew/bin ]]; then
    export PATH="/opt/homebrew/bin:$PATH"
fi

if [[ -d "/Applications/IntelliJ IDEA CE.app/Contents/MacOS" ]]; then
    export PATH="/Applications/IntelliJ IDEA CE.app/Contents/MacOS:$PATH"
fi

export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$SDKMAN_DIR/bin/sdkman-init.sh" ]] && source "$SDKMAN_DIR/bin/sdkman-init.sh"

if [[ -d /opt/homebrew/opt/openjdk@17 ]]; then
    export JAVA_HOME="/opt/homebrew/opt/openjdk@17"
    export PATH="$JAVA_HOME/bin:$PATH"
fi
