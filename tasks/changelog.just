import 'core.just'

# 📋 Get changelog entries (version: <version> | current | unreleased) (default)
[default]
changelog version="current" unreleased="no" plain="no":
    #! ./.shell-wrapper.sh

    version="{{version}}"
    unreleased=$(is_true "{{unreleased}}")
    plain=$(is_true "{{plain}}")

    # Helper functions for styled output and send to stderr
    optional_header() { [[ "$plain" == "true" ]] || header "$1" >&2 ; }
    optional_warn() { [[ "$plain" == "true" ]] || warn "$1" >&2 ; }
    error() { error "$1"; exit 1; }

    content=""
    captured_version=""

    if [[ "$version" == "unreleased" || "$unreleased" == "true" ]]; then
        # Get unreleased changes from git-cliff
        content="$(git cliff --unreleased --bump --strip all | tail -n +2 || true)"
        bumped_version="$(git cliff --bumped-version | tr -d 'v')"
        captured_version="latest: ${bumped_version}"
    else
        input_file="CHANGELOG.md"
        [[ -f "$input_file" ]] || error "File ${input_file} not found."

        if [[ "$version" == "current" ]]; then
            version_header_pattern='^## \[(.*)\]'
        else
            version_header_pattern="^## \[(${version})\]"
        fi

        capture=false
        extracted_content=""

        while IFS= read -r line; do
            if [[ "$line" =~ $version_header_pattern ]] && [[ "$capture" == "false" ]]; then
                captured_version="${BASH_REMATCH[1]}"
                capture=true
                continue
            fi

            if [[ "$capture" == "true" ]]; then
                if [[ "$line" =~ ^##\ \[.*\] ]]; then
                    break
                fi
                extracted_content+="${line}"$'\n'
            fi
        done < "$input_file"

        content="$(echo "$extracted_content" | sed '/^[[:space:]]*$/d')"
    fi

    if [[ -z "$content" ]]; then
        [[ "$plain" == "true" ]] || optional_warn "Nothing found for '${version}'"
        exit 1
    fi

    optional_header "Changelog for '${captured_version}'"
    echo "$content"

# ❓ Show help
[private]
help task="":
    @just-help changelog {{task}}
