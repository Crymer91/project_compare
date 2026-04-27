# Feature Specification: Add CLI Score Descriptions

**Feature Branch**: `[001-add-cli-score-descriptions]`  
**Created**: 2026-04-27  
**Status**: Draft  
**Input**: User description: "Current python script should have human redable description to all aspects at terminal. For example descriptions and examples for scores."

## User Scenarios & Testing

### User Story 1 - Understanding scoring scale (Priority: P1)

Users evaluating software solutions need to understand what each score (0-5) means in practice before answering questions.

**Why this priority**: Without clear scoring guidance, users will give inconsistent or meaningless responses, making the entire comparison unreliable.

**Independent Test**: Can be tested by showing the description system to a new user and verifying they can correctly answer 3 practice questions with consistent scores.

**Acceptance Scenarios**:

1. **Given** a user sees A1 question prompt, **When** they read the description, **Then** they understand that score 0 means "weeks of setup" and score 5 means "works within minutes"
2. **Given** a user sees A2 question prompt, **When** they read the description, **Then** they understand that score 0 requires infrastructure changes and score 5 requires only one PR

---

### User Story 2 - Section context awareness (Priority: P1)

Users need to know why each section matters before evaluating it, so they can weigh their responses appropriately.

**Why this priority**: Sections have different weights (Adoption 25%, Distribution 20%, etc.), and users should understand the relative importance before scoring.

**Independent Test**: Can be tested by presenting a user with section descriptions and verifying they can correctly rank the sections by importance.

**Acceptance Scenarios**:

1. **Given** a user starts the Distribution section, **When** they see the description, **Then** they understand this section evaluates how widely the solution spreads
2. **Given** a user sees "Critical section" warning, **When** they score, **Then** they understand that scores below 0.6 will flag the solution as failed

---

### User Story 3 - Results interpretation (Priority: P2)

After evaluation, users need to understand what their scores mean in practical terms and why certain sections are flagged as critical.

**Why this priority**: Users should leave the evaluation with clear action items, not just numbers.

**Independent Test**: Can be tested by having a user complete an evaluation and explain what the critical section failures mean for their decision.

**Acceptance Scenarios**:

1. **Given** a solution scores 0.4 in Adoption, **When** viewing results, **Then** user understands they should NOT adopt the solution
2. **Given** a section shows "ПРОВАЛ", **When** viewing results, **Then** user sees clear explanation of why this matters and what to do about it

---

### Edge Cases

- What happens when user scores all 3s (the middle)? Show clear indication this represents "average/neutral" performance
- How does system communicate when solution is near threshold (0.55-0.59)? Show warning about borderline status
- How should users handle scoring questions where they have no data? Include guidance for using "unknown" interpretation

## Requirements

### Functional Requirements

- **FR-001**: System MUST display human-readable description of each scoring scale before each question is asked
- **FR-002**: System MUST include practical examples for each score level (0-5) showing what that score represents in real-world terms
- **FR-003**: System MUST display section descriptions and weights before evaluating each section
- **FR-004**: System MUST clearly mark critical sections (Adoption, Distribution, Risk & Trust) and explain threshold implications
- **FR-005**: System MUST show progress indicator for questions within each section
- **FR-006**: Results output MUST include human-readable explanations of what each section score means in practice

### Key Entities

- **Question**: Contains code (A1), primary text (Time-to-first-value), and scale descriptions (0-5 examples)
- **Section**: Contains name, weight, description, and list of questions
- **Scale Description**: Human-readable examples for each score level in a question

## Success Criteria

### Measurable Outcomes

- **SC-001**: New users can correctly answer 3 practice questions with scores within 1 point of an expert evaluation
- **SC-002**: 90% of users correctly identify which sections are critical when asked after evaluation
- **SC-003**: Users complete evaluation with clear understanding of which areas passed/failed (no ambiguous results)
- **SC-004**: Average time to understand scoring guidance is under 30 seconds per section

## Assumptions

- This is a CLI tool (text-only interface), not GUI
- Descriptions should be concise enough to fit on single terminal lines where possible
- Users may run this multiple times, so descriptions should remain helpful on repeat use
- Output language is Russian (as indicated by existing interface)