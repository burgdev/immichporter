import 'core.just'

# ▶️  Run all core quality checks (default)
[default]
all: lock lint deps

# 🔒 Checking uv lock file
lock:
    @header "$(doc check lock)"
    uv lock --locked
    @success "🏁 Lock file checked!"

# 🧹 Linting code"
lint:
    @header "$(doc check lint)"
    uv run pre-commit run -a
    @success "🏁 Linting passed!"


# 🪄  Fixing code with ruff
fix:
    @header "$(doc check fix)"
    uv run ruff check --fix .
    @success "🏁 Fixing passed!"

# 📦 Checking dependencies
deps:
    @header "$(doc check deps)"
    uv run deptry .
    @success "🏁 Dependencies checked!"

# 🔍 Static type checking
types:
    @header "$(doc check types)"
    uv run ty check src
    @success "🏁 Static type checking passed!"

# ❓ Show help
[private]
help task="":
    @just-help check {{task}}
