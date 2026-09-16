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
| FM2-R5-001 | Correct finite-state model for independent gated MLP qualification | PASS |
| R5-NUM-001 | Exhaustive numerical conformance EFSO R5 evaluator ↔ independent QWENRNS batch oracle | PASS |
| FM2-R6-001 | Конечная модель минимального Transformer Block для независимой квалификации | RUNNING |
| R6-NUM-001 | Exhaustive numerical conformance EFSO R6 evaluator ↔ independent QWENRNS batch oracle | RUNNING |

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

Все проверки `FM0-FM3-001` – `E12-001` подтверждены в пределах своих заявленных scopes. `R4-NUM-001` закрывает полный numerical contour из `59049` состояний без mismatches. `E11-001` закрывает изоляцию external witness bridge. `E12-001` закрывает воспроизводимость ранее квалифицированного evidence contour.

R5 contour закрыт: `FM2-R5-001 = PASS`, `R5-NUM-001 = PASS`, `2187` состояний и `2187` external outputs, `mismatch_count = 0` при tolerance `1e-12`.

Текущий R6 contour состоит из `FM2-R6-001` и `R6-NUM-001`. Оба переведены в `RUNNING` до получения фактического CI evidence.

`R7` numerical conformance и NumPy float64 ещё не закрыты.

Новые проверки добавляются только после определения вопроса, конечного пространства и критерия завершения.
