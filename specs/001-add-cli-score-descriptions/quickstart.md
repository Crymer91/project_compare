# Quick Start: Add CLI Score Descriptions

## Running the Updated Tool

```bash
uv run python main.py
```

## Updated Workflow

After applying this feature, the evaluation flow includes:

1. **Header Introduction** (unchanged)
   - Shows tool overview and section weights
   - Lists critical sections and threshold (0.60)

2. **Solution Names** (unchanged)
   - Enter names for two solutions to compare

3. **Section-by-Section Evaluation** (enhanced)
   - Section header shows: name, weight %, description
   - Before each question: shows scale description with practical examples
   - Prompt shows progress: "[A1] 1/4 - Time-to-first-value (0-5)"

4. **Results Display** (enhanced)
   - Shows normalized score with percentage
   - Includes human-readable interpretation (e.g., "Хорошо", "Средне")
   - Critical sections show status (OK / ПРОВАЛ)
   - Borderline scores (0.55-0.59) show warning

## Example Output

### Section Introduction
```
============================================================
Секция: Adoption (вес: 25%)
Описание: Вероятность успешного внедрения решения пользователями
           и скорость получения первой пользы
============================================================
```

### Question with Scale Description
```
[А1] 1/4 - Time-to-first-value (0-5)

Примеры оценок:
  0 - недели настройки до первого результата
  3 - нужно полдня, чтобы увидеть пользу
  5 - работает в течение минут

[А1] Ваша оценка (0-5): 
```

### Results Section
```
────────────────────────────────────────────────────────────
ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ ПО СЕКЦИЯМ:
────────────────────────────────────────────────────────────
Adoption        : 0.75 (75.0%) ████████░░░░░░░░░░ Хорошо
Distribution  : 0.80 (80.0%) █████████░░░░░░░░░░
Economics      : 0.60 (60.0%) ████████░░░░░░░░░░ Средне
Risk & Trust   : 0.55 (55.0%) ███████░░░░░░░░░░░░ Пограничный статус!
```

### Critical Section Warning
```
────────────────────────────────────────────────────────────
⚠️  КРИТИЧЕСКИЕ ЗОНЫ (порог: 0.60):
────────────────────────────────────────────────────────────
❌ Risk & Trust: 0.55 - ПРОВАЛ
   ⚠️ Решение не рекомендуется к внедрению без улучшения
   в области надежности и безопасности
```

## Understanding Scores

| Score Range | Interpretation | Meaning |
|------------|-----------------|----------|
| 0.80-1.00 | Отлично | Сильное решение |
| 0.60-0.79 | Хорошо | Пригодно к использованию |
| 0.40-0.59 | Средне | Требует внимания |
| 0.20-0.39 | Плохо | Не рекомендуется |
| 0.00-0.19 | Очень плохо | Непригодно |

### Critical Sections Extra Guidance

If Adoption, Distribution, or Risk & Trust score below 0.60:
- **ПРОВАЛ** means solution has significant adoption risk
- Consider this failure before proceeding with comparison
- Address the specific concerns before making final decision

## Troubleshooting

**Q: What if I don't know the answer to a question?**
A: Use your best judgment based on the scale descriptions shown. The 0-5 examples help you make an informed decision.

**Q: Why are some sections marked as "critical"?**
A: Critical sections (Adoption 25%, Distribution 20%, Risk & Trust 15%) represent 60% of the total score weight. Failure here makes the solution unsuitable regardless of other scores.

**Q: What does a score of 3 mean?**
A: Score 3 is the middle/neutral option. It means neither particularly good nor bad - the "status quo" or "average" level. This is shown as "Средне" in results.