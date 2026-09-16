# EFSO — ТЕКУЩЕЕ СОСТОЯНИЕ

**Идентификатор:** EFSO-STATE-006  
**Статус:** В РАБОТЕ

## 1. Рабочая граница

Реализация независимого `Exhaustive Finite-State Oracle` для исчерпывающей проверки явно определённых конечных пространств состояний и переходов.

FM0–FM3 structural baseline и E4 exhaustive enumerator закрыты. R4 structural model реализована. Текущая рабочая граница — полная numerical qualification R4 на конечном пространстве `3^10 = 59049`.

## 2. Подтверждено

- `FM0-FM3-001 = PASS`;
- `FM2-R4-001 = PASS` только в пределах исторического structural placeholder scope;
- `E4-001 = PASS`;
- E4 CI run #9: `35044801336`;
- E4 artifact: `efso-e4-001-evidence`, artifact `10425614571`;
- E4 digest: `389351c7d542fa8db7b00041f17fa285629230eff1e8a6c70f8ddaab3baba3df`;
- реализован `src/efso_r4_space.py` с формой `query[2]`, `key[2][2]`, `value[2][2]`;
- для domain `{-1,0,1}` определена structural cardinality `3^10 = 59049`;
- добавлены structural tests `tests/test_r4_space.py`;
- reference contract исправлен по фактической независимой реализации R4;
- добавлен независимый EFSO evaluator `src/efso_r4_evaluator.py`;
- добавлен внешний QWENRNS batch witness `validation/r4_attention_batch_oracle.py`;
- добавлен exhaustive numerical harness `validation/r4_numerical_conformance.py`;
- numerical harness не импортирует QWENRNS, а запускает его только через validation subprocess;
- CI выполняет sparse checkout только требуемого external witness файла;
- machine-readable numerical evidence предусмотрено в `evidence/r4_numerical_conformance.json`.

## 3. Незавершено

- фактический PASS/FAIL CI для `R4-NUM-001`;
- переход `FM2-R4-002` из RUNNING в PASS после фактического evidence;
- E5 independent transition engine;
- E6 exhaustive conformance;
- E7 invariant engine;
- E8 counterexample engine;
- E9 conformance matrix;
- E10 adversarial spaces;
- E11 QWENRNS qualification bridge;
- E12 reproducible verification harness.

## 4. Критическая граница R4

Старая модель `R4State(q, k, v)` с тремя векторами ширины 2 давала `3^6 = 729`, но не соответствовала фактической форме независимого R4 reference. Она не используется как numerical R4 space.

Актуальная модель:

```text
query[2]
key[2][2]
value[2][2]
```

Reference semantics:

```text
score = dot(query, key_row)
weight = exp(score - max(score)) / sum(exp(score - max(score)))
out = sum(weight[row] * value[row])
```

Scaling отсутствует, поскольку его нет в фактическом independent R4 witness.

## 5. Блокирующие условия

EFSO не должен копировать внутреннюю архитектуру IUT или импортировать external oracle в runtime.

`R4-NUM-001 = PASS` запрещён до фактического успешного CI run с `59049` состояниями, `59049` внешними результатами, нулём mismatches и сохранённым artifact.

## 6. Текущая контрольная точка

```text
R4-NUM-001 = RUNNING
```

Последний созданный workflow:

```text
run #31
run_id: 35045105316
head: 69a83110099655a575496655d2549e62011bdd1b
status: QUEUED
```

Он использует sparse checkout external witness.

## 7. Условия закрытия R4 numerical qualification

```text
59049 EFSO states
59049 external outputs
mismatch_count = 0
max_abs_error <= 1e-12
state digest recorded
machine-readable evidence emitted
artifact uploaded
```

## 8. Текущее направление

```text
FM0–FM3 structural baseline
          ↓
E4 exhaustive enumeration = PASS
          ↓
FM2-R4-002 structural alignment
          ↓
R4-NUM-001 = RUNNING
          ↓
E5 independent transition engine
          ↓
E6 exhaustive conformance
          ↓
R5 → R6 → R7 → NumPy float64
          ↓
E7–E12 proof/evidence contour
```
