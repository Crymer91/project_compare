#!/usr/bin/env python3

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# --- Конфигурация модели ---

@dataclass
class Question:
    """Represents a single evaluation metric within a section.
    
    Attributes:
        code: Unique identifier for the question (e.g., 'A1', 'B2').
        text: Human-readable description of what is being evaluated (0-5 scale).
        weight: Weight of this question within its parent section (used for calculating section score).
        scale_description: Human-readable examples for each score level (0-5).
    """
    code: str
    text: str
    weight: float  # вес внутри блока
    scale_description: str = ""  # описания для каждого балла

@dataclass
class Section:
    """Represents a category of evaluation metrics with its own weighted importance.
    
    Attributes:
        name: Section name (e.g., 'Adoption', 'Distribution').
        weight: Overall weight of this section in the final score calculation (e.g., 0.25 for 25%).
        description: Human-readable description of what the section evaluates.
        questions: List of Question objects that belong to this section.
        is_critical: Whether this section is critical (threshold 0.6 applies).
    """
    name: str
    weight: float  # вес блока
    description: str
    questions: List[Question]
    is_critical: bool = False

SECTIONS: List[Section] = [
    Section("Adoption", 0.25, "Вероятность успешного внедрения решения пользователями и скорость получения первой пользы", [
        Question("A1", "Time-to-first-value (0-5)", 1,
            "0 - недели настройки до первого результата\n"
            "3 - нужно полдня, чтобы увидеть пользу\n"
            "5 - работает в течение минут"),
        Question("A2", "Сложность интеграции (0-5)", 1,
            "0 - требует изменений инфраструктуры, одобрения безопасности\n"
            "3 - умеренные усилия по интеграции\n"
            "5 - один PR / изменение конфигурации"),
        Question("A3", "Требования к компетенции (0-5)", 1,
            "0 - требуется эксперт предметной области / создатель\n"
            "3 - инженер среднего уровня\n"
            "5 - джуниор может безопасно работать"),
        Question("A4", "Документация / DX (0-5)", 1,
            "0 - устаревшая / отсутствующая документация\n"
            "3 - пригодно, но требует интерпретации\n"
            "5 - скопировал-вставил - работает"),
    ], is_critical=True),
    Section("Distribution", 0.20, "Насколько широко и легко решение распространяется среди пользователей и интегрируется в процессы", [
        Question("B1", "Встроенность в платформу (0-5)", 1,
            "0 - автономный инструмент\n"
            "3 - опциональный плагин\n"
            "5 - часть CI/CD, шаблонов или платформенного слоя"),
        Question("B2", "Дефолтность (0-5)", 1,
            "0 - требует осознанного решения\n"
            "5 - используется автоматически, если не отключено явно"),
        Question("B3", "Поддержка сверху (0-5)", 1,
            "0 - только инициатива снизу\n"
            "3 - неформальная поддержка\n"
            "5 - обязательно к использованию"),
        Question("B4", "Зависимости других систем (0-5)", 1,
            "0 - изолировано\n"
            "5 - критическая зависимость для множества сервисов"),
    ], is_critical=True),
    Section("Economics", 0.15, "Финансовые аспекты решения: измеримая ценность, стоимость владения и финансовая подотчетность", [
        Question("C1", "Понятная ценность (0-5)", 1,
            "0 - \"кажется полезным\"\n"
            "5 - четкие метрики (время, инциденты, затраты)"),
        Question("C2", "Стоимость владения (0-5)", 1,
            "0 - дорого в эксплуатации и поддержке\n"
            "5 - пренебрежимо малые затраты"),
        Question("C3", "Финансовая модель (0-5)", 1,
            "0 - нет владельца, нет метрик\n"
            "5 - привязано к KPI, showback или бюджетам"),
    ], is_critical=False),
    Section("Risk & Trust", 0.15, "Надежность решения, качество поддержки и соответствие требованиям безопасности", [
        Question("D1", "SLA / надёжность (0-5)", 1,
            "0 - best effort (насколько повезет)\n"
            "5 - формальный SLA с мониторингом"),
        Question("D2", "Поддержка (0-5)", 1,
            "0 - \"напиши автору\"\n"
            "5 - команда-владелец, дежурство по ротации"),
        Question("D3", "Безопасность / compliance (0-5)", 1,
            "0 - заблокировано безопасностью\n"
            "5 - полностью соответствует, предварительно одобрено"),
    ], is_critical=True),
    Section("Switching & Lock-in", 0.10, "Затраты на внедрение решения и сложность отказа от него в будущем (lock-in эффект)", [
        Question("E1", "Стоимость перехода (0-5)", 1,
            "0 - требует значительных усилий\n"
            "5 - минимальные усилия для внедрения"),
        Question("E2", "Стоимость ухода (lock-in) (0-5)", 1,
            "0 - легко уйти\n"
            "5 - очень сложно заменить"),
    ], is_critical=False),
    Section("Product maturity", 0.10, "Зрелость продукта: наличие плана развития, четкость ответственности и скорость обработки обратной связи", [
        Question("F1", "Roadmap (0-5)", 1,
            "0 - нет плана развития\n"
            "5 - понятный roadmap с регулярными релизами"),
        Question("F2", "Ownership (0-5)", 1,
            "0 - один человек\n"
            "5 - выделенная команда"),
        Question("F3", "Обратная связь (0-5)", 1,
            "0 - медленно или нет обратной связи\n"
            "5 - быстро учитываются пожелания"),
    ], is_critical=False),
    Section("Community", 0.05, "Внешняя экосистема: активность сообщества, разнообразие контрибьюторов и прозрачность процессов", [
        Question("G1", "Контрибьюторы (0-5)", 1,
            "0 - единичные контрибьюторы\n"
            "5 - разнообразное активное сообщество"),
        Question("G2", "Процессы (0-5)", 1,
            "0 - непрозрачные процессы\n"
            "5 - структурированные RFC, issues, PR"),
    ], is_critical=False),
]

CRITICAL_SECTIONS = ["Adoption", "Distribution", "Risk & Trust"]
# Секции, которые критически важны для успеха решения.
# Если нормализованный скор любой из этих секций < 0.6, она помечается как ПРОВАЛ.


# --- Логика ---

def ask_score(prompt: str, question_code: str = "", scale_description: str = "", question_number: int = 0, total_questions: int = 0) -> int:
    """Запрашивает у пользователя оценку от 0 до 5.
    
    Аргументы:
        prompt: Текст вопроса, который будет показан пользователю.
        question_code: Код вопроса (например, 'A1') для отображения в prompt.
        scale_description: Описания примеров для каждого балла (0-5).
        question_number: Номер вопроса в секции (1-based).
        total_questions: Всего вопросов в секции.
    
    Возвращает:
        int: Валидная оценка в диапазоне [0, 5].
    
    Примечание:
        Функция циклично запрашивает ввод, пока пользователь не введет
        целое число от 0 до 5. При неверном вводе показывает сообщение об ошибке.
    """
    # Показать описание шкалы перед вопросом
    if scale_description:
        print(f"\nПримеры оценок:")
        for line in scale_description.split('\n'):
            print(f"  {line}")
    
    while True:
        try:
            # Формируем приглашение с прогрессом
            progress = f"[{question_number}/{total_questions}] " if question_number and total_questions else ""
            if question_code:
                value = int(input(f"  [{question_code}] {progress}{prompt}: "))
            else:
                value = int(input(f"{progress}{prompt}: "))
            if 0 <= value <= 5:
                return value
        except ValueError:
            pass
        print("  ⚠️  Введите число от 0 до 5")


def evaluate(solution_name: str) -> Dict:
    """Оценивает одно решение по всем секциям и вопросам.
    
    Аргументы:
        solution_name: Название оцениваемого решения (для вывода в интерфейсе).
    
    Возвращает:
        Dict: Словарь с результатами оценки, содержащий:
            - name: Название решения
            - sections: Словарь {название_секции: нормализованный_скор}
            - final: Итоговый взвешенный скор (0.0 - 1.0)
            - answers: Словарь {код_вопроса: оценка}
    
    Процесс:
        1. Для каждой секции последовательно задает все вопросы
        2. Сохраняет сырые ответы и считает сумму баллов по секции
        3. Нормализует скор секции (делит на максимально возможный)
        4. Считает итоговый скор с учетом весов секций
    """
    print(f"\n=== Оценка решения: {solution_name} ===")
    section_scores = {}
    raw_answers = {}

    for section in SECTIONS:
        print(f"\n{'='*60}")
        print(f"Секция: {section.name} (вес: {section.weight*100:.0f}%)")
        if section.is_critical:
            print(f"⚠️  КРИТИЧЕСКАЯ СЕКЦИЯ")
        print(f"Описание: {section.description}")
        print(f"{'='*60}")
        total = 0
        max_total = 0

        for i, q in enumerate(section.questions, 1):
            score = ask_score(q.text, q.code, q.scale_description, i, len(section.questions))
            raw_answers[q.code] = score
            total += score * q.weight
            max_total += 5 * q.weight

        normalized = total / max_total  # 0..1
        section_scores[section.name] = normalized

    # итоговый скор
    final_score = sum(
        section_scores[s.name] * s.weight for s in SECTIONS
    )

    return {
        "name": solution_name,
        "sections": section_scores,
        "final": final_score,
        "answers": raw_answers
    }


def get_score_interpretation(score: float, is_critical: bool = False) -> str:
    """Возвращает человекочитаемую интерпретацию оценки секции.
    
    Аргументы:
        score: Нормализованная оценка (0.0 - 1.0).
        is_critical: Является ли секция критической.
    
    Возвращает:
        str: Интерпретация на русском языке.
    """
    if 0.55 <= score < 0.60 and is_critical:
        return "Пограничный статус - требует внимания"
    elif 0.60 <= score < 0.80:
        return "Хорошо"
    elif score >= 0.80:
        return "Отлично"
    elif score >= 0.40:
        return "Средне"
    else:
        return "Требует внимания"


def print_result(result: Dict):
    """Выводит результаты оценки одного решения в читаемом формате.
    
    Аргументы:
        result: Словарь с результатами (формат, возвращаемый функцией evaluate).
    
    Выводит:
        - Итоговый скор решения
        - Скор по каждой секции
        - Статус критических зон (OK или ПРОВАЛ согласно порогу 0.6)
    """
    print(f"\n{'='*60}")
    print(f"РЕЗУЛЬТАТЫ ОЦЕНКИ: {result['name']}")
    print(f"{'='*60}")
    print(f"\n📊 Итоговый скор: {result['final']:.2f} из 1.00")
    print(f"   {'●' * int(result['final'] * 20)}{'○' * (20 - int(result['final'] * 20))}")

    print(f"\n{'─'*60}")
    print("ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ ПО СЕКЦИЯМ:")
    print(f"{'─'*60}")
    for section in SECTIONS:
        score = result["sections"][section.name]
        percentage = score * 100
        bar = '█' * int(score * 20) + '░' * (20 - int(score * 20))
        interpretation = get_score_interpretation(score, section.is_critical)
        print(f"{section.name:20}: {score:.2f} ({percentage:5.1f}%) {bar} {interpretation}")

    # критические провалы
    print(f"\n{'─'*60}")
    print("⚠️  КРИТИЧЕСКИЕ ЗОНЫ (порог: 0.60):")
    print(f"{'─'*60}")
    failed_critical = []
    for section in SECTIONS:
        if section.is_critical:
            val = result["sections"][section.name]
            status = "ПРОВАЛ" if val < 0.6 else "OK"
            icon = "❌" if val < 0.6 else "✅"
            print(f"{icon} {section.name:20}: {val:.2f} - {status}")
            if val < 0.6:
                failed_critical.append(section.name)
    
    if failed_critical:
        print(f"\n⚠️  РЕКОМЕНДАЦИЯ: Не внедряйте решение без улучшения")
        print(f"   в следующих критических областях: {', '.join(failed_critical)}")
    
    # Вывод ответов
    print(f"\n{'─'*60}")
    print("ДЕТАЛИ ОТВЕТОВ:")
    print(f"{'─'*60}")
    for code, score in result["answers"].items():
        print(f"  {code}: {score}")


def compare(r1: Dict, r2: Dict):
    """Сравнивает два решения и выводит победителя.
    
    Аргументы:
        r1: Результаты первого решения (из evaluate).
        r2: Результаты второго решения (из evaluate).
    
    Выводит:
        - Итоговые скоры обоих решений
        - Название победителя (решение с большим скором)
        - Разницу по каждой секции (положительная = r1 лучше, отрицательная = r2 лучше)
    """
    print(f"\n{'='*60}")
    print(f"СРАВНЕНИЕ РЕШЕНИЙ")
    print(f"{'='*60}")

    print(f"\n📊 Итоговые результаты:")
    print(f"  • {r1['name']}: {r1['final']:.2f} ({r1['final']*100:.1f}%)")
    print(f"  • {r2['name']}: {r2['final']:.2f} ({r2['final']*100:.1f}%)")

    winner = r1 if r1["final"] > r2["final"] else r2
    loser = r2 if winner == r1 else r1
    diff_total = abs(r1["final"] - r2["final"])
    
    print(f"\n🏆 ПОБЕДИТЕЛЬ: {winner['name']}")
    print(f"   Преимущество: {diff_total:.2f} баллов ({diff_total*100:.1f}%)")

    print(f"\n{'─'*60}")
    print("ДЕТАЛЬНОЕ СРАВНЕНИЕ ПО СЕКЦИЯМ:")
    print(f"{'─'*60}")
    print(f"{'Секция':20} │ {'Разница':>10} │ {'Лидер':>15}")
    print(f"{'─'*20}─┼{'─'*10}─┼{'─'*15}")
    
    for section in r1["sections"]:
        diff = r1["sections"][section] - r2["sections"][section]
        leader = r1['name'] if diff > 0 else r2['name'] if diff < 0 else "Ничья"
        icon = "▲" if diff > 0 else "▼" if diff < 0 else "="
        print(f"{section:20} │ {icon} {diff:+8.2f} │ {leader:>15}")


# --- Entry point ---

def main():
    """Точка входа в приложение.
    
    Процесс:
        1. Запрашивает названия двух решений для сравнения
        2. Последовательно оценивает каждое решение (все 21 вопрос)
        3. Выводит детальные результаты по каждому решению
        4. Сравнивает решения и объявляет победителя
    
    Примечание:
        Весь пользовательский интерфейс на русском языке.
        Для ввода требуется нажатие Enter после каждой оценки.
    """
    print(f"\n{'='*60}")
    print(f"  СИСТЕМА СРАВНЕНИЯ ПРОГРАММНЫХ РЕШЕНИЙ")
    print(f"{'='*60}")
    print(f"\nЭтот инструмент помогает объективно сравнить два решения")
    print(f"на основе 21 критерия в 7 категориях:")
    print(f"\n  • Adoption (25%)      - Внедрение пользователями")
    print(f"  • Distribution (20%)   - Распространение решения")
    print(f"  • Economics (15%)      - Финансовые аспекты")
    print(f"  • Risk & Trust (15%)   - Надежность и безопасность")
    print(f"  • Switching (10%)      - Стоимость смены решения")
    print(f"  • Product maturity (10%) - Зрелость продукта")
    print(f"  • Community (5%)       - Экосистема и сообщество")
    print(f"\n⚠️  Критические секции (порог 0.60): Adoption, Distribution, Risk & Trust")
    print(f"{'='*60}\n")

    name1 = input("Введите название решения 1: ")
    name2 = input("Введите название решения 2: ")

    print(f"\n{'='*60}")
    print(f"НАЧАЛО ОЦЕНКИ РЕШЕНИЙ")
    print(f"{'='*60}")

    r1 = evaluate(name1)
    r2 = evaluate(name2)

    print_result(r1)
    print_result(r2)

    compare(r1, r2)
    
    # Финальное резюме
    print(f"\n{'='*60}")
    print(f"ИТОГОВОЕ РЕЗЮМЕ")
    print(f"{'='*60}")
    winner = r1 if r1["final"] > r2["final"] else r2
    print(f"\n✅ Рекомендуется к внедрению: {winner['name']}")
    print(f"   Итоговый скор: {winner['final']:.2f}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()