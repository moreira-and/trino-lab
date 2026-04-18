SHELL := /bin/bash

.PHONY: help init-env render-config up start

help:
	@echo "Usage: make <target>"
	@echo "Available targets:"
	@echo "  init-env      - Create .env from .env.example if .env does not exist"
	@echo "  render-config - Generate Trino configuration files from .env"
	@echo "  up            - Generate config and start services via docker compose"
	@echo "  start         - Initialize .env, generate config and start services"
	@echo "  help          - Show this help message"

init-env:
	@if [ -f .env ]; then \
		echo ".env already exists. Edit it if needed."; \
	else \
		cp .env.example .env && echo "Created .env from .env.example"; \
	fi

render-config:
	@python3 scripts/render-config.py

up: render-config
	@docker compose -f compose.yaml up -d

start: init-env up
	@echo "Services started. Use 'docker compose -f compose.yaml ps' to verify."