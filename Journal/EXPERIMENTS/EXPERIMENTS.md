# EFSO — РЕЕСТР ПРОВЕРОК

Реестр содержит только идентификаторы, назначение, статус и ссылки на отдельные документы результатов.

| ID | Проверка | Статус |
|---|---|---|
| FM0-FM3-001 | Первый исполняемый structural qualification contour: formal boundary, independence, finite-state model, exact structural properties | PASS |
| FM2-R4-001 | Первое конечное пространство R4: cardinality, canonical identity, exhaustive enumeration model | PASS |
| E4-001 | Универсальный exhaustive enumerator: exact cardinality, uniqueness, duplicate detection, replay order | RUNNING |

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

`FM0-FM3-001` и `FM2-R4-001` подтверждают structural baseline и конечную модель R4. `E4-001` реализован и ожидает выполнения в CI; полное численное сравнение с внешним R4 reference, R5–R7, NumPy float64 и E5–E12 ещё не закрыты.

Новые проверки добавляются только после определения вопроса, конечного пространства и критерия завершения.
