import 'core.just'

# 📋 Run tests
[default]
tests parallel="no":
    #! ./.shell-wrapper.sh
    header $(doc tests)
    parallel=$(is_true "{{parallel}}")
    if [[ "$parallel" == "true" ]]; then
        pytest -v -n auto
    else
        pytest -v
    fi
