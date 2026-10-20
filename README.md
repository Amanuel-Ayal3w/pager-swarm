# Pager

Incident-response agent swarm. This scaffold is the API and the operator UI shell. Agents are not wired yet.

Postgres database `pager` and Redis run on the host. Connection settings live in `.env` (see `.env.example`). `SRS.md` and the style folder are local reference only.

```bash
uv sync
make db
make api
```

The API listens on `http://127.0.0.1:8000`. `GET /api/health` checks Postgres and Redis.

```bash
cd web && npm install
make web
```

The UI listens on `http://127.0.0.1:3000`. `make dev` starts both.

`make seed` loads ten Faker incidents, one for every state. `INC-1048` is a T2 rollback (`rollback api`) and `INC-1042` is a T1 restart. `make simulate` plays one new incident onto the live feed.
