# ============================================================
# Steam Deck
# ============================================================

[[ -d "$HOME/Emulation" ]] &&
    alias emu='cd ~/Emulation'

[[ -d "$HOME/Emulation/roms" ]] &&
    alias roms='cd ~/Emulation/roms'

[[ -d "$HOME/Emulation/bios" ]] &&
    alias bios='cd ~/Emulation/bios'

[[ -d "$HOME/homebrew" ]] &&
    alias decky='cd ~/homebrew'  # decky: open the Decky homebrew directory

decky_version() {  # decky: show the installed Decky Loader version
    local version_file="$HOME/homebrew/services/.loader.version"

    if [[ ! -r "$version_file" ]]; then
        echo "decky_version: Decky Loader version file not found" >&2
        return 1
    fi

    command cat "$version_file"
}

decky_status() {  # decky: show Decky Loader service status
    systemctl status plugin_loader --no-pager
}

decky_restart() {  # decky: restart Decky Loader and show its status
    sudo systemctl restart plugin_loader &&
        systemctl status plugin_loader --no-pager --lines=12
}

decky_logs() {  # decky: show recent Decky logs; pass -f to follow
    if [[ "$1" == "-f" ]]; then
        journalctl --unit=plugin_loader --follow --output=cat
    else
        journalctl --unit=plugin_loader --lines="${1:-100}" --no-pager --output=cat
    fi
}

decky_plugins() {  # decky: list installed Decky plugins and authors
    local plugins_dir="$HOME/homebrew/plugins"

    if [[ ! -d "$plugins_dir" ]]; then
        echo "decky_plugins: Decky plugin directory not found" >&2
        return 1
    fi

    if command -v jq >/dev/null 2>&1; then
        find "$plugins_dir" -mindepth 2 -maxdepth 2 -name plugin.json \
            -exec jq -r '"\(.name)\t\(.author)"' {} + | sort
    else
        find "$plugins_dir" -mindepth 1 -maxdepth 1 -type d \
            -exec basename {} \; | sort
    fi
}

decky_update() {  # decky: download and run the latest stable Decky installer
    if ! command -v curl >/dev/null 2>&1; then
        echo "decky_update: curl is required" >&2
        return 1
    fi

    local installer exit_code
    installer=$(mktemp "${TMPDIR:-/tmp}/decky-installer.XXXXXX") || return 1

    curl --fail --location --show-error \
        "https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/install_release.sh" \
        --output "$installer"
    exit_code=$?

    if (( exit_code == 0 )); then
        chmod +x "$installer"
        exit_code=$?
    fi

    if (( exit_code == 0 )); then
        sh "$installer"
        exit_code=$?
    fi

    command rm -f "$installer"
    return "$exit_code"
}
