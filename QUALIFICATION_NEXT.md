# Следующий этап qualification

## Текущее состояние

R4, R5 и R6 qualification contours закрыты в пределах явно определённых finite spaces и подтверждённого evidence.

Последнее закрытие:

```text
FM2-R6-001 = PASS
R6-NUM-001 = PASS
6561 states
6561 external outputs
mismatch_count = 0
tolerance = 1e-12
```

## Следующий обязательный контур

```text
R7-NUM-001
```

Порядок реализации строго соответствует `REDMI.md`:

1. определить и зафиксировать корректное R7 finite-state qualification space;
2. проверить cardinality, canonical identity и deterministic enumeration;
3. определить независимый external-origin R7 witness;
4. зафиксировать source commit и Git blob SHA;
5. создать source-exact pinned snapshot без runtime dependency на внешний repository;
6. реализовать независимый EFSO-side R7 evaluator;
7. выполнить exhaustive state-by-state numerical comparison;
8. зафиксировать tolerance до запуска;
9. сформировать machine-readable evidence и artifact;
10. только после фактического CI PASS закрыть `R7-NUM-001` и синхронизировать `EXPERIMENTS.md`, `МАЯК.md` и `CURRENT_STATE.md`.

## Запрет перехода

Наличие R7 в дорожной карте не является основанием считать R7 начатым или завершённым.

```text
ROADMAP
   ↓
DEFINED
   ↓
RUNNING
   ↓
CI / evidence
   ↓
PASS
   ↓
state synchronization
```

Статус не может быть сильнее имеющегося evidence.

## После R7

После закрытия `R7-NUM-001` остаётся отдельная qualification axis:

```text
NumPy float64
```

NumPy `float64` не является частью EFSO runtime и не трактуется как exact real arithmetic oracle.
