import 'core.just'

# 🌐 Serve docu for preview (default)
[default]
serve port='8088':
    @header "$(doc docs serve)"
    @info "Serving at 'localhost:{{port}}'."
    uv run --group docs mkdocs serve --dev-addr localhost:{{port}}

# 📦 Build docu
build:
    @header "$(doc docs build)"
    uv run --group docs mkdocs build
    @success "🏁 Documentation build in 'site' directory."

# ❓ Show help
[private]
help task="":
    @just-help docs {{task}}
