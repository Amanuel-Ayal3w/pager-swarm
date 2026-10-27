.PHONY: db api web dev seed simulate investigate approve target eval

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

investigate:
	uv run python -m pager.graph.run --scenario bad_deploy

approve:
	uv run python -m pager.graph.run --latest --approve

target:
	uv run uvicorn pager.target.app:app --host 127.0.0.1 --port 8010

eval:
	uv run python -m evals.runner --model $(if $(MODEL),$(MODEL),scripted)
