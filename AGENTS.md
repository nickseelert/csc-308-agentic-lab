# Agent instructions

Read `VISION.md` first. Keep changes small: one issue, one branch, one PR.

## Layout
- `data/` committed Statcast snapshot (`postseason_2026.csv.gz`, `players.csv`). Do not edit by hand.
- `analysis/` pure Python. `load.py` loads data; `metrics.py` holds one function per metric.
- `analysis/build_site_data.py` writes `site/data/*.json`, which the site imports.
- `site/` Next.js static export. `app/page.tsx` is the page; `lib/data.ts` types the JSON.
- `tests/` pytest. Every new metric gets a test.

## Commands
```
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/ruff check . && .venv/bin/ruff format --check .
.venv/bin/pytest -q
.venv/bin/python -m analysis.build_site_data
cd site && npm ci && npx tsc --noEmit && npm run build
```
All of these must pass before you open or update a PR. CI runs the same steps (`test` check).

## Rules
- Never add network calls, secrets, tokens or new services.
- Never weaken, skip or delete a test to make CI pass. Fix the code or explain in the PR.
- New metric: add a function to `metrics.py`, a test, an entry in `build_site_data.py`, a type in
  `lib/data.ts`, and a section on the page.
- Raw Statcast `player_name` is the pitcher. Use `pitcher_name` / `batter_name`.
- PR description: what changed, why, how it was verified, and a link to the issue (`Closes #N`).
- If the request is unclear or out of scope, ask on the issue instead of guessing.
