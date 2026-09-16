# EFSO — ТЕКУЩЕЕ СОСТОЯНИЕ

**Идентификатор:** EFSO-STATE-004  
**Статус:** В РАБОТЕ

## 1. Рабочая граница

Реализация независимого `Exhaustive Finite-State Oracle` для исчерпывающей проверки явно определённых конечных пространств состояний и переходов.

Текущая граница включает FM0–FM3 structural baseline и закрытый E4 exhaustive enumerator. Следующая граница — корректная семантическая модель R4 перед numerical conformance.

## 2. Подтверждено

- создан отдельный репозиторий EFSO;
- определено назначение EFSO как независимого verification-контура;
- зафиксировано ограничение exhaustive-проверки конечным пространством `F`;
- создан нормативный Journal EFSO;
- NumPy, C и другие внешние numerical oracle не являются частью EFSO runtime;
- EFSO не зависит от IUT;
- реализован `src/efso_fm03.py` как минимальный FM0–FM3 structural contour;
- завершён `FM0-FM3-001` со статусом `PASS`;
- конечное базовое пространство 3×3 имеет `|F| = 9`;
- реализован `src/efso_exhaustive.py` для exact cardinality, uniqueness, duplicate detection и replay-order verification;
- добавлены тесты `tests/test_exhaustive.py`;
- добавлен CI workflow `.github/workflows/tests.yml`;
- E4 evidence generator `validation/e4_001_evidence.py` добавлен в CI;
- E4-001 закрыт фактическим CI run #9 с 9/9 тестами PASS и machine-readable artifact;
- E4 enumeration digest для `E4-BASE-3x3` зафиксирован как `389351c7d542fa8db7b00041f17fa285629230eff1e8a6c70f8ddaab3baba3df`;
- `E4-001 = PASS`;
- исторический `FM2-R4-001 = PASS` сохранён без переписывания истории, но его scope ограничен structural placeholder-space;
- зарегистрирован `FM2-R4-002` для проверки соответствия формы R4 finite-state model фактической Attention semantics независимого reference.

## 3. Незавершено

- `FM2-R4-002`: корректная форма и cardinality R4 finite-state space;
- полноценное независимое numerical сравнение R4 с внешним QWENRNS reference;
- независимый transition engine E5;
- exhaustive conformance E6;
- invariant engine E7;
- counterexample engine E8;
- conformance matrix E9;
- adversarial spaces E10;
- QWENRNS qualification bridge E11;
- reproducible verification harness E12.

## 4. Важное исправление границы R4

Текущий structural placeholder `R4State(q, k, v)` с тремя векторами ширины 2 даёт `3^6 = 729` состояний, но не соответствует форме независимого R4 Attention reference, где используются `query[2]`, `key[2][2]` и `value[2][2]`.

Следовательно, `729` не может использоваться как доказанная cardinality numerical R4 space. До E6 необходимо определить и проверить корректную finite-state shape. Это не отменяет закрытый E4.

## 5. Блокирующие условия

EFSO не должен копировать внутреннюю архитектуру IUT или импортировать external oracle в runtime.

R4 numerical PASS не может быть объявлен до появления фактического независимого reference comparison evidence и корректной finite-state model.

## 6. Последнее подтверждённое состояние

```text
FM0-FM3-001 = PASS
FM2-R4-001  = PASS (structural placeholder scope)
E4-001      = PASS
FM2-R4-002  = PLANNED
```

## 7. Следующая контрольная точка

**FM2-R4-002 → R4 semantic shape alignment**

Цель: определить минимальное конечное пространство, которое действительно соответствует независимой primitive Attention semantics.

Условие закрытия:

```text
R4 state shape defined
exact cardinality derived
canonical identity defined
finite enumeration reproducible
reference semantics aligned
machine-readable evidence emitted
```

## 8. Evidence E4

```text
CI run: #9
run_id: 35044801336
commit: 267bdff265fd3f713bccdb06db9285c4cc25e89e
artifact: efso-e4-001-evidence
artifact_id: 10425614571
artifact_sha256: 95d6a03571bd69dbeea4b977cf370d8812abe520d14b68e11a9ec07b3c100411
```

## 9. Текущее направление

```text
FM0–FM3 structural baseline
          ↓
E4 exhaustive enumeration = PASS
          ↓
FM2-R4-002 semantic shape alignment
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
