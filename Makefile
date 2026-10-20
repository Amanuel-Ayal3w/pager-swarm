.PHONY: db api web dev seed simulate

db:
	uv run python -c "from pager.storage.db import init_db; init_db(); print('tables ready')"

api:
	uv run uvicorn pager.api.main:app --host 127.0.0.1 --port 8000 --reload

web:
	cd web && npm run dev

dev:
	uv run uvicorn pager.api.main:app --host 127.0.0.1 --port 8000 & pid=$$!; \
	trap 'kill $$pid' EXIT INT TERM; \
	cd web && npm run dev

seed:
	uv run python -m pager.dev.seed

simulate:
	uv run python -m pager.dev.simulator
