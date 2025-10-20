import 'core.just'

# supported sync_args: "--all-groups", "--no-dev", "--group <group>"

# 📦 Install the uv environment and install the pre-commit hooks.
install sync_args="--all-groups":
    @header "$(doc project install)"
    cd {{justfile_dir()}}; uv sync {{sync_args}}
    cd {{justfile_dir()}}; uv run pre-commit install


# 🚀 Prepare a release, update CHANGELOG file and bump versions
release add_tag="no" dry="no" unreleased="yes" length="-1":
    #! ./.shell-wrapper.sh
    header "$(doc project release)"
    new_tag=$(uv run git-cliff --bumped-version)
    new_version="${new_tag#v}"  # Remove 'v' prefix

    if is_true "{{dry}}"; then
        # Handle unreleased flag
        if is_true "{{unreleased}}"; then
            info "Show only 'unreleased' changes"
        else
            if [ "{{length}}" -gt 0 ]; then
                info "Show {{length}} lines of changelog"
            else
                info "Show full changelog"
            fi
        fi

        header "Changelog start"

        # Build git-cliff command
        cmd="uv run git-cliff --bump"
        if is_true "{{unreleased}}"; then
            cmd="$cmd --unreleased"
        fi

        # Get changelog
        cl=$(eval "$cmd")

        # Output appropriate portion of changelog
        if is_true "{{unreleased}}" || [ "{{length}}" -le 0 ]; then
            echo "$cl"
        else
            echo "$cl" | head -n "{{length}}"
            echo "..."
        fi

        header "Changelog end"
    else
        # Update CHANGELOG.md and bump version
        uv run git-cliff --bump -u --prepend CHANGELOG.md
        uv run bump2version --new-version "$new_version" patch

        if [ -n "$new_tag" ]; then
            success "Bumped to version '$new_version' (tag '$new_tag')."
            info "Please check the entries in 'CHANGELOG.md' and update it accordingly."

            if is_true "{{add_tag}}"; then
                git tag -f "$new_tag"
                git push origin "$new_tag"
            fi
            warn "Did not update to new version tag."
        fi
    fi


# 🔢 Print current or next project version
version next="no":
    #! ./.shell-wrapper.sh
    version="unknown"
    pyproject_toml_file="{{justfile_dir()}}/pyproject.toml"

    # Read version from pyproject.toml
    if [ -f "$pyproject_toml_file" ]; then
        # Try to get version from project.version first
        version=$(grep -E '^version\s*=' "$pyproject_toml_file" | head -1 | cut -d'"' -f2 2>/dev/null)

        # If not found, try to get from tool.poetry.version
        if [ -z "$version" ]; then
            version=$(grep -A 1 '\[tool\.poetry\]' "$pyproject_toml_file" | grep 'version = ' | head -1 | cut -d'"' -f2 2>/dev/null)
        fi
    fi

    if is_true "{{next}}"; then
        new_version=$(git-cliff --bumped-version | tr -d 'v')
        if [ "$new_version" = "$version" ]; then
            warn "No newer version available"
        fi
        echo "$new_version"
    else
        echo "$version"
    fi

# 🔄 Update immich client to a specific version
update_immich_client version="2.0.1":
    #! /usr/bin/env bash
    version="${version//v/}"  # Remove 'v' prefix if present
    url="https://raw.githubusercontent.com/immich-app/immich/refs/tags/v${version}/open-api/immich-openapi-specs.json"
    output="src/immichporter/immich/client/"

    uv run openapi-python-client generate --url "$url" --meta none --output-path "$output" --overwrite
    success "Updated immich client to version '${version}'."

# ❓ Show help
[private]
[default]
help task="":
    @just-help project {{task}}
