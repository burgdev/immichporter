import 'core.just'

# 📋 Run tests
[default]
tests parallel="no":
    #! ./.shell-wrapper.sh
    parallel=$(is_true "{{parallel}}")
    header "Running tests"
    if [[ "$parallel" == "true" ]]; then
        pytest -v -n auto
    else
        pytest -v
    fi
