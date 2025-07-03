.DEFAULT_GOAL := help
DC = docker compose

# BASE DOCKER COMMANDS
up: ## Build and start all services except certbot in detached mode.
	docker compose up --build -d --no-deps $(shell docker compose config --services)

down: ## Stop and remove all running services.
	${DC} down

restart: ## Restart all running services to apply any changes.
	${DC} restart

build: ## Rebuild all services, ensuring the latest changes are included.
	${DC} build

full-build: ## Build all services without using the cache, ensuring a fresh build.
	${DC} build --no-cache

logs: ## Display logs for all services, useful for monitoring and debugging.
	${DC} logs --follow

# HELP
.PHONY: help
help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@awk 'BEGIN {FS = ":.*?## "; section=""; prev_section=""} \
		/^[#].*/ { \
			section = substr($$0, 3); \
		} \
		/^[a-zA-Z0-9_-]+:.*?## / { \
			if (section != prev_section) { \
				print ""; \
				print "\033[1;34m" section "\033[0m"; \
				prev_section = section; \
			} \
			gsub(/\\n/, "\n                      \t\t"); \
			printf " \x1b[36;1m%-28s\033[0m%s\n", $$1, $$2; \
		}' $(MAKEFILE_LIST)
