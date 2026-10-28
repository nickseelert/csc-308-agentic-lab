# csc-308-agentic-lab

Live demo for a University of Toronto **CSC308 (Technology Leadership)** guest lecture on agentic
software development.

A team of AI agents, each its own [Hermes Agent](https://hermes-agent.nousresearch.com) profile on
a different model, builds this site from student suggestions:

1. **Orchestrator** turns a request into a GitHub issue and a task on a Kanban board.
2. **Developer** implements it on a branch, runs the tests and opens a pull request.
3. **Reviewer**, a different model from a different vendor, checks out the PR, reruns the checks and
   approves or requests changes.
4. **Integrator** merges once the approval matches the latest commit and CI is green.
5. GitHub Pages redeploys the site.

Everything the agents did is public: see the issues, pull requests and reviews in this repo.

- Site: https://nickseelert.github.io/csc-308-agentic-lab/
- Data: MLB Statcast for the 2026 postseason via [pybaseball](https://github.com/jldbc/pybaseball),
  committed as a snapshot so builds never depend on the network.
- Agent rules: [`AGENTS.md`](AGENTS.md) and [`VISION.md`](VISION.md).

## Run it yourself
```
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest -q
.venv/bin/python -m analysis.build_site_data
cd site && npm ci && npm run dev
```
