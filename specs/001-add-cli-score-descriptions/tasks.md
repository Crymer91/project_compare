# Tasks: Add CLI Score Descriptions

**Feature**: `001-add-cli-score-descriptions`  
**Spec**: [spec.md](spec.md)  
**Plan**: [plan.md](plan.md)

---

## Overview

Total Tasks: 15

## Implementation Strategy

The feature follows an incremental approach:
- **MVP (User Story 1)**: Core scale descriptions displayed before each question
- **Incremental (User Story 2)**: Add section context and progress indicator
- **Polish (User Story 3 + Edge Cases)**: Results interpretation and edge case handling

---

## Phase 1: Setup

No setup tasks required - project already exists with main.py.

---

## Phase 2: Foundational

These tasks modify the core data structures needed by all user stories.

- [X] T001 Add `scale_description` field to Question dataclass in main.py
- [X] T002 Add `is_critical` field to Section dataclass in main.py
- [X] T003 Define SCALE_DESCRIPTIONS constant with Russian strings for all 21 questions (A1-G2)

---

## Phase 3: User Story 1 - Understanding Scoring Scale (P1)

**Goal**: Display human-readable scale descriptions (0-5 examples) before each question is asked.

**Independent Test**: Show description system to new user, verify they can correctly answer 3 practice questions with scores within 1 point of expert evaluation.

### Implementation Tasks

- [X] T004 [P] [US1] Update Question dataclass to include scale_description in main.py
- [X] T005 [US1] Modify ask_score() in main.py to display scale description before prompting
- [X] T006 [US1] Validate all 21 questions have scale descriptions displayed

---

## Phase 4: User Story 2 - Section Context Awareness (P1)

**Goal**: Display section descriptions and weights before evaluating each section, with progress indicator.

**Independent Test**: Present section descriptions to user, verify they can correctly rank sections by importance.

### Implementation Tasks

- [X] T007 [P] [US2] Add is_critical flag to Section dataclass in main.py
- [X] T008 [US2] Modify evaluate() function to display section header with weight percentage
- [X] T009 [US2] Add progress indicator (e.g., "[A1] 1/4") to question prompts in evaluate()

---

## Phase 5: User Story 3 - Results Interpretation (P2)

**Goal**: Results output includes human-readable explanations of what each section score means.

**Independent Test**: Have user complete evaluation, verify they can explain what critical section failures mean.

### Implementation Tasks

- [X] T010 [P] [US3] Add section_interpretations to evaluation result structure in main.py
- [X] T011 [US3] Implement get_score_interpretation() helper in main.py
- [X] T012 [US3] Modify print_result() to show human-readable interpretations and critical warnings

---

## Phase 6: Edge Cases & Polish

Handle edge cases identified in feature spec.

- [X] T013 Handle score=3 display as "Средний балл" in results interpretation
- [X] T014 Add borderline warning for scores 0.55-0.59
- [X] T015 Integrate all changes and verify end-to-end flow

---

## Dependencies

```
T001 ──┬── T004 ──> US1 Complete
T002 ──┤          │
T003 ──┘          ▼
             T005 ──> T007 ──> US2 Complete
                           │
             T006 ──────────┘
                           ▼
             T008 ──> T010 ──> US3 Complete
             T009 ────────────┘
                           ▼
             T011 ──> T013 ─> Edge Cases Complete
             T012 ───────────┘
                           ▼
             T014 ──────────────> All Tasks Complete
             T015 ─────────────────��────┘
```

---

## Parallel Opportunities

| Task | Can Run In Parallel With |
|------|---------------------|
| T001, T002, T003 | Independent setup tasks |
| T004, T007, T010 | Each adds field to different dataclass |
| T005, T008, T011 | Different functions in main.py |

---

## Independent Test Criteria by User Story

| User Story | Test Criteria |
|-----------|----------------|
| US1 - Scoring Scale | New user can answer 3 practice questions with consistent scores after seeing descriptions |
| US2 - Section Context | User can rank sections by importance after viewing section headers |
| US3 - Results | User can explain what critical section failures mean for their decision |

---

## Suggested MVP Scope

Implement User Story 1 (US1) only:
- T001, T002, T003: Foundational data structure updates
- T004, T005, T006: Scale descriptions before questions

This delivers core value: users understand what each score means before answering.