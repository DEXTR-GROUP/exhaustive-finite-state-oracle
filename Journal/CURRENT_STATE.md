# EFSO — ТЕКУЩЕЕ СОСТОЯНИЕ

**Идентификатор:** EFSO-STATE-014  
**Статус:** В РАБОТЕ

## 1. Рабочая граница

Реализация независимого `Exhaustive Finite-State Oracle` для исчерпывающей проверки явно определённых конечных пространств состояний и переходов.

FM0–FM3, E4, R4 numerical qualification, E5, E6, E7, E8, E9, E10, E11, E12 и R5 qualification закрыты в пределах заявленных scopes. Текущая рабочая граница: R6 numerical qualification.

## 2. Подтверждено

- `FM0-FM3-001 = PASS`;
- `FM2-R4-001 = PASS` только в пределах исторического structural placeholder scope;
- `FM2-R4-002 = PASS`;
- `E4-001 = PASS`;
- `R4-NUM-001 = PASS`: `59049` состояний, `59049` external outputs, `mismatch_count = 0`, `max_abs_error = 0.0`;
- `E5-001 = PASS`: 11 независимых операторов, без внешних runtime dependencies;
- `E6-001 = PASS`;
- `E7-001 = PASS`;
- `E8-001 = PASS`;
- `E9-001 = PASS`;
- `E10-001 = PASS`;
- `E11-001 = PASS`;
- `E12-001 = PASS` в пределах ранее квалифицированного evidence contour;
- `FM2-R5-001 = PASS`: конечное пространство gated MLP `3^7 = 2187`;
- `R5-NUM-001 = PASS`: `2187` состояний, `2187` external outputs, `mismatch_count = 0`, `max_abs_error = 0.0`, tolerance `1e-12`;
- CI run `35052989511`, commit `b665bc99361fd83de3a00de05fb3849ecc5cd90b`, job `104657174952` завершён успешно;
- artifact `efso-qualification-evidence`: ID `10429760824`, SHA-256 `ae7bccc89ac9f65d295efaefbd14b6114090dbff3eca686742ada3935ba7194f`.

## 3. Реализовано для R6

- `src/efso_r6_space.py`: конечное пространство `3^8 = 6561`;
- `src/efso_r6_evaluator.py`: независимый EFSO-side R6 evaluator;
- `validation/witnesses/r6_transformer_batch_oracle.py`: source-exact snapshot external-origin QWENRNS witness;
- `validation/witnesses/R6_WITNESS_MANIFEST.json`: provenance source commit + source Git blob SHA;
- `validation/fm2_r6_001_evidence.py`: structural evidence конечного пространства;
- `validation/r6_numerical_conformance.py`: exhaustive state-by-state comparison с fixed tolerance `1e-12` и проверкой provenance snapshot;
- CI расширен запуском FM2-R6-001 и R6-NUM-001.

## 4. R6 reference provenance

```text
source repository = DEXTR-GROUP/QWENRNS
source path       = validation/r6_transformer_batch_oracle.py
source commit     = a40bdbfd999535f2bb9c57da6f2a2e861e49c12c
source blob       = dcea89f0c6246d1f466a91f696c3091d8e9c8948
```

Исходный QWENRNS witness расширен отдельным batch-интерфейсом; EFSO использует его source-exact snapshot без runtime checkout внешнего repository.

## 5. Незавершено

- фактическое CI evidence для `FM2-R6-001`;
- фактическое CI evidence для `R6-NUM-001`;
- `R7-NUM-001`;
- NumPy float64 qualification.

## 6. Текущая контрольная точка

```text
FM2-R6-001 = RUNNING
R6-NUM-001 = RUNNING
```

## 7. Условия закрытия R6-NUM-001

```text
6561 EFSO states
6561 external outputs
verified source provenance
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
FM2-R5-001 = PASS
      ↓
R5-NUM-001 = PASS
      ↓
FM2-R6-001 = RUNNING
      ↓
R6-NUM-001 = RUNNING
      ↓
R7-NUM-001
      ↓
NumPy float64
```
