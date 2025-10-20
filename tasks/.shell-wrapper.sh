#!/usr/bin/env bash
set -eu -o pipefail
# get soruce (follow symlinks)
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  # If the symlink was relative, resolve it relative to the symlink's directory
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
export TERM="xterm-256color"
cd "$(dirname "$SOURCE")"/..
source "tasks/shell-source.sh"
bash "$@"
