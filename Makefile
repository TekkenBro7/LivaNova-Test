UV = uv run
UVICORN = uv run uvicorn

GREEN = \033[0;32m
YELLOW = \033[1;33m
NC = \033[0m

HOST ?= 0.0.0.0
PORT ?= 8000

.PHONY: help run lint format test

help:
	@echo "$(YELLOW)Available targets:$(NC)"
	@echo "  $(GREEN)run$(NC)           - Start FastAPI development server"
	@echo "  $(GREEN)lint$(NC)          - Run ruff linter"
	@echo "  $(GREEN)format$(NC)        - Format code with ruff"
	@echo "  $(GREEN)test$(NC)          - Run tests"

run:
	@echo "$(GREEN)Starting FastAPI server...$(NC)"
	$(UVICORN) src.main:app --reload --host $(HOST) --port $(PORT)

lint:
	@echo "$(GREEN)Running linters...$(NC)"
	$(UV) ruff check .
	$(UV) mypy .

format:
	@echo "$(GREEN)Formatting code with ruff...$(NC)"
	$(UV) ruff format .

test:
	@echo "$(GREEN)Running tests...$(NC)"
	$(UV) pytest
