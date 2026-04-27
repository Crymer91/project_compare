# Research: Add CLI Score Descriptions

## Decision 1: Scale Description Format

**Decision**: Embed scale descriptions as inline text before each question prompt.

**Rationale**: 
- The Question dataclass already has a `text` field containing the question prompt
- Existing code comments (lines 40-64 in main.py and similar across all questions) already contain Russian scale descriptions
- These can be extracted and displayed before asking for input
- Maintains CLI simplicity - displayed as text, no UI changes needed

**Alternatives considered**:
- Store descriptions in separate JSON/YAML file - rejected: adds file complexity, more points of failure
- Add tooltip or help command - rejected: doesn't fit single-CLI-interaction model
- Use colored output - rejected: may not render on all terminals

---

## Decision 2: Section Context Display

**Decision**: Display section header with name, weight percentage, and description at start of each section.

**Rationale**:
- Section dataclass already contains `name`, `weight`, and `description` fields
- Currently printed in evaluate() function but without weight emphasis
- Adding weight percentage (e.g., "(вес: 25%)") clarifies importance per constitution requirement
- Section description already exists in Russian, needs only to be shown prominently

---

## Decision 3: Progress Indicator

**Decision**: Show "Question X of Y" format in the prompt line.

**Rationale**:
- Simple numeric indicator fits standard CLI patterns
- Can be added to the prompt string displayed to users
- No additional state tracking needed - questions list has known length per section

**Alternatives considered**:
- Percentage completion bar - rejected: takes too much screen space
- Dots/stars indicator - rejected: less informative than exact numbers

---

## Decision 4: Results Output Enhancement

**Decision**: Add human-readable interpretation to section scores in results.

**Rationale**:
- User Story 3 requires understanding what scores mean in practice
- Currently shows raw normalized score (e.g., "0.75")
- Should add interpretation such as "Хорошо", "Средне", "Требует внимания"
- Critical sections (Adoption, Distribution, Risk & Trust) need explicit explanation when < 0.6

---

## Decision 5: Edge Case Handling

**Decision**: Handle middle score (3) and borderline threshold (0.55-0.59) explicitly.

**Rationale**:
- Edge cases specified in feature spec require explicit handling
- Score 3 shows as "Средний балл" (Average)
- Scores 0.55-0.59 show warning "Пограничный статус" (Borderline status)

---

## Implementation Notes

### Existing Scale Descriptions (extracted from main.py comments)

| Question | Score 0 | Score 3 | Score 5 |
|----------|---------|---------|--------|
| A1 (Time-to-first-value) | недели настройки | полдня для пользы | работает в минутах |
| A2 (Сложность интеграции) | изменения инфраструктуры | умеренные усилия | один PR |
| A3 (Требования к компетенции) | нужен эксперт | инженер среднего уровня | джуниор может работать |
| A4 (Документация / DX) | устаревшая/отсутствует | пригодно, но требует интерпретации | скопировал-вставил - работает |
| B1 (Встроенность в платформу) | автономный инструмент | опциональный плагин | часть CI/CD |
| B2 (Дефолтность) | требует осознанного решени�� | - | используется автоматически |
| B3 (Поддержка сверху) | только инициатива снизу | неформальная поддержка | обязательно к использованию |
| B4 (Зависимости других систем) | изолировано | - | критическая зависимость |
| C1 (Понятная ценность) | "кажется полезным" | - | четкие метрики |
| C2 (Стоимость владения) | дорого в эксплуатации | - | пренебрежимо малые затраты |
| C3 (Финансовая модель) | нет владельца, нет метрик | - | привязано к KPI |
| D1 (SLA / надёжность) | best effort | - | формальный SLA |
| D2 (Поддержка) | "напиши автору" | - | команда-владелец |
| D3 (Безопасность) | заблокировано безопасностью | - | полностью соответствует |
| E1 (Стоимость перехода) | требует значительных усилий | - | минимальные усилия |
| E2 (Стоимость ухода) | легко уйти | - | очень сложно заменить |
| F1 (Roadmap) | нет плана | - | понятный план развития |
| F2 (Ownership) | один человек | - | выделенная команда |
| F3 (Обратная связь) | медленно | - | быстро учитывается |
| G1 (Контрибьюторы) | единичные | - | разнообразное сообщество |
| G2 (Процессы) | непрозрачные | - | структурированные RFC |

## Summary of Changes Required

1. **Question dataclass**: Add optional `scale_description` field (or use existing text field differently)
2. **evaluate() function**: Display section header with context, scale description before each question
3. **print_result() function**: Add human-readable interpretation of scores
4. **Edge case handling**: Add special messages for score 3 and borderline threshold

**No external integrations or dependencies required** - pure extension of existing functionality.