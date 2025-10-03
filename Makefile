.PHONY: init
init: ## Install the uv environment and install the pre-commit hooks
	@echo "Creating virtual environment using uv"
	@uv sync --dev
	@ uv run invoke install --venv-update

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := init
