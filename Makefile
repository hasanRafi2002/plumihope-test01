.PHONY: up down logs migrate seed backend-test web-test

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose exec api alembic upgrade head

seed:
	docker compose exec api python scripts/seed.py

backend-test:
	docker compose exec api pytest

web-test:
	cd web && npm test
