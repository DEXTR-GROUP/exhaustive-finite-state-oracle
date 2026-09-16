# EFSO — ТЕКУЩЕЕ СОСТОЯНИЕ

**Идентификатор:** EFSO-STATE-012  
**Статус:** В РАБОТЕ

## 1. Рабочая граница

Реализация независимого `Exhaustive Finite-State Oracle` для исчерпывающей проверки явно определённых конечных пространств состояний и переходов.

FM0–FM3, E4, R4 numerical qualification, E5, E6, E7, E8, E9, E10, E11 и E12 закрыты в пределах заявленных scopes. Текущая рабочая граница: R5 numerical qualification.

## 2. Подтверждено

- `FM0-FM3-001 = PASS`;
- `FM2-R4-001 = PASS` только в пределах исторического structural placeholder scope;
- `FM2-R4-002 = PASS`;
- `E4-001 = PASS`;
- `R4-NUM-001 = PASS`: `59049` состояний, `59049` external outputs, `mismatch_count = 0`, `max_abs_error = 0.0`;
- `E5-001 = PASS`: 11 независимых операторов, без внешних runtime dependencies;
- `E6-001 = PASS`: полный R4 state-by-state conformance contour;
- `E7-001 = PASS`: `59049` состояний, 4 инварианта, 0 нарушений;
- `E8-001 = PASS`: deterministic extraction и minimization воспроизводимого counterexample;
- `E9-001 = PASS`: coverage matrix, 5 квалифицированных строк;
- `E10-001 = PASS`: 7 adversarial finite spaces;
- `E11-001 = PASS`: external witness bridge изолирован, mutation independence подтверждена;
- `E12-001 = PASS`: два последовательных прогона полного evidence contour дали идентичные return codes, stdout/stderr digests и канонический evidence digest;
- CI baseline `35048841379`, commit `a426212ac5a29ee3f94fa507b3fd9550bb53b1b4`, job `104644596946` завершён успешно; artifact `10428436038`, SHA-256 `12b5271373be5c0de3056ad9538871a36e6ddd8c0df7e1a0c7b4a3482b5f6079`.

## 3. Реализовано для текущей точки R5

- `src/efso_r5_space.py`: явное конечное пространство `3^7 = 2187`;
- `src/efso_r5_evaluator.py`: независимый EFSO-side R5 evaluator;
- `validation/witnesses/r5_mlp_batch_oracle.py`: immutable snapshot external-origin QWENRNS witness;
- `validation/witnesses/R5_WITNESS_MANIFEST.json`: provenance source commit + source Git blob SHA;
- `validation/fm2_r5_001_evidence.py`: структурное evidence конечного пространства;
- `validation/r5_numerical_conformance.py`: exhaustive state-by-state comparison с fixed tolerance `1e-12` и проверкой provenance snapshot;
- CI больше не делает checkout приватного QWENRNS. R4 и R5 qualification используют pinned local witness snapshots.

## 4. Текущая инфраструктурная причина изменения

Предыдущая схема CI пыталась выполнять `actions/checkout` для приватного `DEXTR-GROUP/QWENRNS`. Runner возвращал `Repository not found`. `ref: main` устранил только разрешение default branch и подтвердил фактический блокирующий уровень: отсутствие доступа runner к приватному repository.

Замена QWENRNS другим oracle не выполнялась. External-origin identity сохранена через pinned snapshot и provenance verification.

## 5. Незавершено

- закрытие `FM2-R5-001` по CI evidence;
- закрытие `R5-NUM-001` по фактическому CI evidence;
- R6 numerical qualification;
- R7 numerical qualification;
- NumPy float64 qualification.

## 6. Текущая контрольная точка

```text
FM2-R5-001 = RUNNING
R5-NUM-001 = RUNNING
```

## 7. Условия закрытия R5-NUM-001

```text
explicit finite R5 state space
independent EFSO R5 evaluator
external-origin pinned witness snapshot
verified source provenance
exhaustive enumeration of the declared space
actual result count == expected cardinality
mismatch_count == 0
max_abs_error <= 1e-12
machine-readable evidence
CI success
artifact uploaded
```

## 8. Текущее направление

```text
FM0–FM3 = PASS
      ↓
E4 = PASS
      ↓
R4-NUM-001 = PASS
      ↓
E5 = PASS
      ↓
E6 = PASS
      ↓
E7 = PASS
      ↓
E8 = PASS
      ↓
E9 = PASS
      ↓
E10 = PASS
      ↓
E11 = PASS
      ↓
E12 = PASS
      ↓
FM2-R5-001 = RUNNING
      ↓
R5-NUM-001 = RUNNING
      ↓
R6-NUM-001
      ↓
R7-NUM-001
      ↓
NumPy float64
```
