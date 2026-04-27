# Data Model: Add CLI Score Descriptions

## Entities

### Question (Modified)

Represents a single evaluation metric within a section.

| Field | Type | Description |
|-------|------|-------------|
| code | str | Unique identifier (e.g., 'A1', 'B2') |
| text | str | Question prompt in Russian (e.g., "Time-to-first-value (0-5)") |
| weight | float | Weight within parent section (1.0 typically) |
| scale_description | str | **NEW** - Human-readable examples for each score 0-5 |

**Validation Rules**: None (text field only, no parsing)

**State Transitions**: N/A (static data structure)

---

### Section (Modified)

Represents a category of evaluation metrics.

| Field | Type | Description |
|-------|------|-------------|
| name | str | Section name (e.g., 'Adoption', 'Distribution') |
| weight | float | Weight in final score calculation (e.g., 0.25 for 25%) |
| description | str | Human-readable description of what the section evaluates |
| questions | List[Question] | Questions in this section |
| is_critical | bool | **NEW** - Whether this is a critical section (threshold applies) |

**Validation Rules**: None

---

### ScaleDescription (New - Embedded in Question)

Human-readable interpretation of each score level.

| Score | Meaning | Example Messages |
|-------|---------|-------------------|
| 0 | Worst | "недели настройки", "требует изменений инфраструктуры" |
| 1 | Very Poor | - |
| 2 | Poor | "нуждается в улучшении" |
| 3 | Average | "умеренные усилия", "средний уровень" |
| 4 | Good | - |
| 5 | Best | "работает в минутах", "скопировал-вставил - работает" |

---

### EvaluationResult (Modified)

Results of evaluating a single solution.

| Field | Type | Description |
|-------|------|-------------|
| name | str | Solution name |
| sections | Dict[str, float] | Section codes to normalized scores (0-1) |
| final | float | Final weighted score (0-1) |
| answers | Dict[str, int] | Raw question codes to scores (0-5) |
| section_interpretations | Dict[str, str] | **NEW** - Human-readable interpretations |

---

## Data Flow

```
User Input → Section Header Display → Question Prompt + Scale Description 
→ Score Input (validated 0-5) → Store in answers → Calculate section score
→ Calculate final score → Results Display with interpretations
```

---

## Relationships

- **One Section has Many Questions** (1:N)
- **One EvaluationResult has Many SectionScores** (1:N)
- **ScaleDescriptions are embedded in Question** (composition)

---

## Validation Rules (from Feature Spec)

- Scores MUST be integers 0-5 inclusive
- Input validation already enforced in ask_score()
- Descriptions shown BEFORE input request

---

## Edge Cases

| Edge Case | Handling Display |
|-----------|------------------|
| Score = 3 | "Средний балл" in results interpretation |
| Section score 0.55-0.59 | "Пограничный статус - требует внимания" warning |
| Score < 0.6 in critical section | "ПРОВАЛ" with explanation of implications |