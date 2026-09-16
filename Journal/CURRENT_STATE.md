# EFSO — ТЕКУЩЕЕ СОСТОЯНИЕ

**Идентификатор:** EFSO-STATE-003  
**Статус:** В РАБОТЕ

## 1. Рабочая граница

Реализация независимого `Exhaustive Finite-State Oracle` для исчерпывающей проверки явно определённых конечных пространств состояний и переходов.

Текущая граница включает FM0–FM3 structural baseline и реализацию E4 exhaustive enumerator.

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
- добавлен CI workflow `.github/workflows/tests.yml` для автоматического выполнения тестов;
- R4 qualification space формально определён как `3^6 = 729` состояний;
- удалён устаревший локальный numerical adapter `src/r4_qualification.py`, который не соответствовал полноценной Attention semantics;
- `src/efso_r4_qualification.py` оставлен structural-only: внешний reference остаётся вне EFSO runtime;
- E4 зарегистрирован в Journal как `RUNNING` до фактического CI evidence.

## 3. Незавершено

- фактическое выполнение E4 в CI и сохранение machine-readable evidence;
- полноценное независимое numerical сравнение R4 с внешним QWENRNS reference;
- независимый transition engine E5;
- exhaustive conformance E6;
- invariant engine E7;
- counterexample engine E8;
- conformance matrix E9;
- adversarial spaces E10;
- QWENRNS qualification bridge E11;
- reproducible verification harness E12.

## 4. Блокирующие условия

EFSO не должен копировать внутреннюю архитектуру IUT или импортировать external oracle в runtime.

R4 numerical PASS не может быть объявлен до появления фактического независимого reference comparison evidence. Наличие 729 перечисленных состояний само по себе numerical conformance не доказывает.

## 5. Последнее подтверждённое состояние

```text
FM0-FM3-001 = PASS
FM2-R4-001  = PASS
E4-001       = RUNNING
```

## 6. Следующая контрольная точка

**E4-001 → CI evidence**

Цель: фактически выполнить exhaustive enumerator и подтвердить exact cardinality, uniqueness, duplicate rejection и replay-order determinism.

Условие закрытия:

```text
CI run exists
all E4 tests PASS
machine-readable evidence emitted
E4 registry status can move to PASS
```

## 7. Текущее направление

```text
FM0–FM3 structural baseline
          ↓
E4 exhaustive enumeration
          ↓
R4 structural qualification
          ↓
R4 independent numerical conformance
          ↓
R5 → R6 → R7
          ↓
NumPy float64
          ↓
E7–E12 proof/evidence contour
```
