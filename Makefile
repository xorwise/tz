build:
	@echo "Building..."
	@docker compose --env-file ./app/.env --build

run:
	@echo "Running..."
	@docker compose --env-file ./app/.env up -d

stop:
	@echo "Stopping..."
	@docker compose down

watch:
	@echo "Watching..."
	@docker compose --env-file ./app/.env up -d && docker compose logs -f server
