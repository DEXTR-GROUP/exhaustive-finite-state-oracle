# EFSO — РЕЕСТР ПРОВЕРОК

Реестр содержит только идентификаторы, назначение, статус и ссылки на отдельные документы результатов.

| ID | Проверка | Статус |
|---|---|---|
| FM0-FM3-001 | Первый исполняемый structural qualification contour: formal boundary, independence, finite-state model, exact structural properties | PASS |
| FM2-R4-001 | Первое конечное пространство R4: cardinality, canonical identity, exhaustive enumeration model | PASS |
| E4-001 | Универсальный exhaustive enumerator: exact cardinality, uniqueness, duplicate detection, replay order | PASS |
| FM2-R4-002 | Корректное соответствие формы конечного R4-space независимой Attention semantics | PASS |
| R4-NUM-001 | Exhaustive numerical conformance EFSO R4 evaluator ↔ independent QWENRNS batch oracle | PASS |
| E5-001 | Independent deterministic transition engine | PASS |
| E6-001 | Qualification of generic exhaustive conformance contour on full R4 finite space | PASS |
| E7-001 | Independent exhaustive invariant engine qualification | PASS |
| E8-001 | Independent deterministic counterexample extraction and minimization engine | PASS |
| E9-001 | Machine-readable conformance coverage matrix | PASS |
| E10-001 | Adversarial finite-space qualification | PASS |
| E11-001 | External witness qualification bridge and mutation-independence boundary | PASS |
| E12-001 | Reproducible verification harness | PASS |

## Правила реестра

- одна проверка получает один стабильный ID;
- одна самостоятельная проверка имеет отдельный документ результата;
- изменение протокола после запуска не переписывает предыдущую запись;
- `PLANNED`, `RUNNING`, `PASS`, `FAIL`, `INCONCLUSIVE` отражают фактическое состояние;
- реестр не содержит интерпретацию вместо первичного evidence.

## Жизненный цикл

```text
PLANNED
   ↓
RUNNING
   ├── PASS
   ├── FAIL
   └── INCONCLUSIVE
```

## Последнее состояние

Все проверки `FM0-FM3-001` – `E12-001` в текущем квалификационном контуре подтверждены в пределах своих заявленных scopes. `R4-NUM-001` закрывает полный numerical contour из `59049` состояний без mismatches. `E11-001` закрывает изоляцию external witness bridge по фактическому CI evidence. `E12-001` закрывает воспроизводимость полного набора из десяти qualification commands: два последовательных прогона дали одинаковые return codes, stdout/stderr digests и канонический evidence digest.

`R5/R6/R7` numerical conformance и NumPy float64 ещё не закрыты.

Новые проверки добавляются только после определения вопроса, конечного пространства и критерия завершения.
