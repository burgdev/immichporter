import 'core.just'

# ⚡ Code quality tasks (lint, fix, types, deps, ...)
mod check
# 📋 Run tests (pytest)
mod tests
# 📚 Documentation tasks (build, serve, ...)
mod docs
# 📦 Project tasks (install, release, ...)
mod project
# 📝 Show next changelog entries
mod changelog

# ❓ Show help (just help [group] [task])
[default]
help group="" task="":
    #! ./.shell-wrapper.sh
    echo "Run tasks with '{{BLUE}}just <group> <task> [params]{{NORMAL}}'."
    echo
    echo "Parameters are added as positional arguments."
    echo "{{YELLOW + BOLD}}Examples:{{NORMAL}}"
    echo "    {{BLUE}}just check{{NORMAL}}"
    echo "    {{BLUE}}just project release yes no{{NORMAL}}"
    echo "    {{BLUE}}just project update_immich_client 2.0.1{{NORMAL}}"
    echo "    {{BLUE}}just help check{{NORMAL}}"
    echo
    just-help {{group}} {{task}}
