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
| E8-001 | Independent deterministic counterexample extraction and minimization engine | RUNNING |

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

`FM0-FM3-001`, `FM2-R4-001`, `E4-001`, `FM2-R4-002`, `R4-NUM-001`, `E5-001`, `E6-001` и `E7-001` подтверждены в пределах своих заявленных scopes. `R4-NUM-001` закрывает полный numerical contour из `59049` состояний без mismatches. `E5-001` закрывает собственный independent transition engine. `E6-001` закрывает generic exhaustive conformance contour на полном R4 finite space. `E7-001` закрывает independent invariant engine на полном R4 finite space.

`E8-001` квалифицирует механизм извлечения и минимизации контрпримеров на детерминированном finite fixture. Его статус ожидает фактического CI evidence.

`R5/R6/R7` numerical conformance, NumPy float64 и E9–E12 ещё не закрыты.

Новые проверки добавляются только после определения вопроса, конечного пространства и критерия завершения.
