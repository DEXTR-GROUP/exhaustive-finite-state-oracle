# EFSO — ТЕКУЩЕЕ СОСТОЯНИЕ

**Идентификатор:** EFSO-STATE-005  
**Статус:** В РАБОТЕ

## 1. Рабочая граница

Реализация независимого `Exhaustive Finite-State Oracle` для исчерпывающей проверки явно определённых конечных пространств состояний и переходов.

FM0–FM3 structural baseline и E4 exhaustive enumerator закрыты. Текущая рабочая граница — `FM2-R4-002`: корректная конечная модель primitive Attention перед numerical conformance.

## 2. Подтверждено

- `FM0-FM3-001 = PASS`;
- `FM2-R4-001 = PASS` только в пределах исторического structural placeholder scope;
- `E4-001 = PASS`;
- E4 CI run #9: `35044801336`;
- E4 artifact: `efso-e4-001-evidence`, artifact `10425614571`;
- E4 digest: `389351c7d542fa8db7b00041f17fa285629230eff1e8a6c70f8ddaab3baba3df`;
- добавлен `src/efso_r4_space.py` с формой `query[2]`, `key[2][2]`, `value[2][2]`;
- для domain `{-1,0,1}` новая R4 structural cardinality определена как `3^10 = 59049`;
- добавлены `tests/test_r4_space.py`;
- добавлен внешний shape contract `validation/r4_reference_contract.json` без импорта external oracle в EFSO runtime;
- добавлен `validation/fm2_r4_002_evidence.py`;
- evidence generation включён в CI.

## 3. Незавершено

- фактический CI evidence для `FM2-R4-002`;
- numerical R4 conformance с независимым QWENRNS reference;
- E5 independent transition engine;
- E6 exhaustive conformance;
- E7 invariant engine;
- E8 counterexample engine;
- E9 conformance matrix;
- E10 adversarial spaces;
- E11 QWENRNS qualification bridge;
- E12 reproducible verification harness.

## 4. Критическая граница R4

Старая модель `R4State(q, k, v)` с тремя векторами ширины 2 давала `3^6 = 729`, но не соответствовала форме независимого R4 reference. Она не используется как numerical R4 space.

Новая structural model использует:

```text
query[2]
key[2][2]
value[2][2]
```

и содержит 10 конечных scalar parameters, следовательно:

```text
|F| = 3^10 = 59049
```

Это пока structural shape alignment. Численная семантика ещё не квалифицирована.

## 5. Блокирующие условия

EFSO не должен копировать внутреннюю архитектуру IUT или импортировать external oracle в runtime.

R4 numerical PASS запрещён до появления независимого numerical comparison evidence.

## 6. Текущая контрольная точка

```text
FM2-R4-002 = RUNNING
```

Условие закрытия:

```text
CI PASS
shape alignment PASS
authorized cardinality = 59049
unique = 59049
missing = 0
duplicates = 0
machine-readable evidence emitted
```

## 7. Текущее направление

```text
FM0–FM3 structural baseline
          ↓
E4 exhaustive enumeration = PASS
          ↓
FM2-R4-002 = RUNNING
          ↓
R4 independent numerical conformance
          ↓
E5 independent transition engine
          ↓
E6 exhaustive conformance
          ↓
R5 → R6 → R7 → NumPy float64
          ↓
E7–E12 proof/evidence contour
```
