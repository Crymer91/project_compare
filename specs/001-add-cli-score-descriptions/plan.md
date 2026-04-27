# Implementation Plan: Add CLI Score Descriptions

**Branch**: `001-add-cli-score-descriptions` | **Date**: 2026-04-27 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `spec.md`

## Summary

Add human-readable score descriptions to the CLI evaluation tool. The system will display:
- Scale descriptions (0-5 examples) before each question is asked
- Section context with weights before each section starts
- Progress indicator showing question number within section
- Human-readable explanations in results output
- Clear critical section warnings below 0.6 threshold

This feature modifies existing data structures (Question, Section) and I/O functions (ask_score, evaluate, print_result) to include descriptive text while maintaining Russian localization.

## Technical Context

**Language/Version**: Python 3.11+ (uses dataclasses, type hints, f-strings)  
**Primary Dependencies**: None (pure Python standard library)  
**Storage**: N/A (in-memory evaluation tool)  
**Testing**: Not currently defined in project  
**Target Platform**: CLI (cross-platform: Windows, macOS, Linux via `uv run python main.py`)  
**Project Type**: Interactive CLI tool for weighted decision framework evaluation  
**Performance Goals**: Fast interactive input, minimal overhead (<100ms per prompt)  
**Constraints**: All output in Russian, input must be integers 0-5, Enter-key input only  
**Scale/Scope**: 21 questions across 7 sections, evaluates 2 solutions per run

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Weighted Decision Framework | ✅ PASS | Core requirement - tool uses 7 sections with defined weights |
| Input Validation (0-5 integers) | ✅ PASS | ask_score validates range and integer type |
| Critical Section Flagging (<0.6) | ✅ PASS | CRITICAL_SECTIONS aligned with constitution |
| Russian Localization | ✅ PASS | All new user-facing text will be in Russian |
| CLI Simplicity | ✅ PASS | Uses Enter-key input only |

## Project Structure

### Documentation (this feature)

```text
specs/001-add-cli-score-descriptions/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── contracts/           # Phase 1 output (N/A - internal CLI tool)
```

### Source Code (repository root)

```text
main.py                 # Entry point - run via `uv run python main.py`
AGENTS.md              # Agent context (references plan)
.specify/              # SpecKit configuration
```

**Structure Decision**: Single-file CLI tool (main.py). Feature adds descriptions to existing Question and Section data structures - no additional files needed in source project.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
