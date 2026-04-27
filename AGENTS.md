# AGENTS.md

## Running the project

```bash
uv run python main.py
```

This is an interactive CLI tool for comparing software solutions using a weighted decision framework.

## How it works

1. Prompts for two solution names
2. Scores each across 21 questions (0-5 scale) across 7 sections
3. Calculates weighted final score
4. Flags critical sections (Adoption, Distribution, Risk & Trust) if normalized score < 0.6

## Architecture

- `main.py` - Entry point, contains all scoring logic and data structures
- `context.txt` - Full decision framework documentation (not needed for running)

## Key sections (weights)

- Adoption (25%): A1-A4
- Distribution (20%): B1-B4
- Economics (15%): C1-C3
- Risk & Trust (15%): D1-D3
- Switching (10%): E1-E2
- Product Maturity (10%): F1-F3
- Community (5%): G1-G2

## Important quirks

- Input requires Enter key - no special key handling
- Scores must be integers 0-5, validates input
- All output is in Russian (interface, prompts, results)

<!-- SPECKIT START -->
**Plan**: `specs/001-add-cli-score-descriptions/plan.md`
- Research: `specs/001-add-cli-score-descriptions/research.md`
- Data Model: `specs/001-add-cli-score-descriptions/data-model.md`
- Quick Start: `specs/001-add-cli-score-descriptions/quickstart.md`
<!-- SPECKIT END -->
