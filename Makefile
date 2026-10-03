.DEFAULT_GOAL := help
.PHONY: help setup lint format test up down restart logs dev clean

COMPOSE := docker compose

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

setup: ## Install test/dev dependencies
	python3 -m pip install -r requirements.test.txt

lint: ## Run ruff lint and format checks
	ruff check .
	ruff format . --check

format: ## Auto-format and auto-fix with ruff
	ruff format .
	ruff check . --fix

test: ## Run the test suite
	python3 -m pytest

up: ## Start Home Assistant (Docker) in the background
	$(COMPOSE) up -d

down: ## Stop and remove the Home Assistant container
	$(COMPOSE) down

restart: ## Restart Home Assistant to pick up integration changes
	$(COMPOSE) restart

logs: ## Follow the Home Assistant logs
	$(COMPOSE) logs -f homeassistant

dev: up logs ## Start Home Assistant and follow its logs

clean: ## Remove caches and coverage artifacts
	rm -rf .pytest_cache .ruff_cache .coverage coverage.xml
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
