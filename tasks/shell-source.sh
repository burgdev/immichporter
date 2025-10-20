#!/usr/bin/env bash

# =========================
# ANSI color codes
# =========================
# Format: \033[<attr>;<fg>m
# Attr (style):
#   0  -> reset / normal
#   1  -> bold
# Foreground colors:
#   30 -> black
#   31 -> red
#   32 -> green
#   33 -> yellow
#   34 -> blue
#   36 -> cyan
# Example:
#   "\033[1;33mHello\033[0m"  → bold yellow text
# =========================

# =========================
# Logging / helper functions
# Hard-coded ANSI codes (colors + bold)
# =========================

info()    { printf "\033[1;36minfo:\033[0m %s\n" "$1"; }       # Bold cyan
success() { printf "\033[1;32mok:\033[0m %s\n" "$1"; }         # Bold green
warn()    { printf "\033[1;33mwarn:\033[0m %s\n" "$1"; }       # Bold yellow
error()   { printf "\033[1;31merror:\033[0m %s\n" "$1"; }      # Bold red

doc() { just help $1 $2 | grep -o "#.*" | sed "s/^#\s//"; }

# Header: 80 characters wide, text left-aligned, padded with =
header() {
    local text="$1"
    local total=80
    local padding_len=$(( total - 6 - ${#text} ))  # 6 for "==== " + " ===="
    if (( padding_len < 0 )); then padding_len=0; fi
    local padding=$(printf '=%.0s' $(seq 1 $padding_len))
    printf "\033[1;34m==== %s %s\033[0m\n" "$text" "$padding"
}

# Section: 80 characters wide, left-aligned
section() {
    local text="$1"
    local total=80
    local padding_len=$(( total - 4 - ${#text} - 4 )) # 4 for "-- " + " --"
    if (( padding_len < 0 )); then padding_len=0; fi
    local padding=$(printf '=%.0s' $(seq 1 $padding_len))
    printf "\033[1;33m-- %s %s\033[0m\n" "$text" "$padding"
}
just-help() {
    local group="$1"
    local task="$2"
    printf "\033[1;33mAvailable tasks:\033[0m\n"
    if [ -n "$task" ]; then
        text=$(just --list "$group" --list-submodules --unsorted | grep "$task" | tail -n +2)
    elif [ -n "$group" ]; then
        if [ "$group" == "all" ]; then
            text=$(just --list --list-submodules --unsorted | tail -n +2)
        else
            text=$(just --list "$group" --list-submodules --unsorted | tail -n +2)
        fi
    else
        text=$(just --list --unsorted | tail -n +2)
    fi
    BLUE="\033[34m"
    RESET="\033[0m"
    YELLOW="\033[33m"

    printf "%s\n" "$text" | awk -v yellow="$YELLOW" -v blue="$BLUE" -v reset="$RESET" '
    {
      split($0, parts, "#")
      if ($1 ~ /:$/) {
        printf "%s%s%s\n", yellow,  $0, reset
      } else if (length(parts) > 1) {
        # Replace # with desired symbol (optional)
        sub(/^#/, "│", $0)
        printf "%s%s%s%s\n", parts[1], blue, parts[2], reset
      } else {
        print $0
      }
    }'
}

is_true() {
    local val="$1"
    case "${val,,}" in
        y|yes|true|1|on) return 0 ;;
        *) return 1 ;;
    esac
}

# Returns 0 (true) if input is no/n/false/0 (case-insensitive)
is_false() {
    local val="$1"
    case "${val,,}" in
        n|no|false|0|off) return 0 ;;
        *) return 1 ;;
    esac
}

export -f info header section error warn success just-help doc is_true is_false
