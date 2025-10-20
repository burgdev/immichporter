#set allow-duplicate-variables
set shell := ["./.shell-wrapper.sh", "-c"]


## Show help for a specific task or list all tasks
#[default]
#help task="":
#    #!/usr/bin/env bash
#    if [ -z "{{task}}" ]; then
#        just -l --unsorted
#    else
#        just --show {{task}} | grep '^#' | sed 's/^\s*#\s*//'
#    fi
