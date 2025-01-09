.PHONY: help install-micromamba build-env setup-env install-poetry install-uv init-uv sync-dependencies
.DEFAULT_GOAL := help

PROJECT = ailedeau
MICROMAMBA_BIN = $(HOME)/.local/bin/micromamba
UV_BIN = $(HOME)/.local/bin/uv
PATH_ADDITION = export PATH=$(HOME)/.local/bin:$$PATH;

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-uv: ## Install uv (Python virtual environment manager)
	@if [ ! -x "$(UV_BIN)" ]; then \
		echo "uv not found, installing..."; \
		curl -Ls https://raw.githubusercontent.com/direnv/uv/main/install.sh | bash -s -- -b $(HOME)/.local/bin; \
	else \
		echo "uv is already installed."; \
	fi
	@echo "Adding uv to PATH for subsequent commands."

init-uv: install-uv ## Initialize virtual environment using uv (ignoring workspace)
	@$(PATH_ADDITION) $(UV_BIN) init --no-workspace $(PROJECT) && \
		echo "Virtual environment initialized for project $(PROJECT) without workspace."

sync-dependencies: ## Sync dependencies between [tool.poetry.dependencies] and [project] sections in pyproject.toml
	@echo "Syncing dependencies..."
	python3 sync_dependencies.py
	@echo "Dependencies synced successfully!"

