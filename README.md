# Exhaustive Finite-State Oracle (EFSO)

Независимый verification-контур для исчерпывающей проверки конечных пространств состояний и вычислительных переходов.

EFSO не является реализацией IUT и не импортирует IUT, NumPy oracle или C oracle. Exhaustive-проверка распространяется только на явно определённые конечные пространства.

## Текущий статус

**В РАБОТЕ — R4, R5 и R6 qualification закрыты в пределах заявленных finite spaces; следующая контрольная точка — R7-NUM-001.**

Подтверждённая последовательность:

```text
FM0–FM3 = PASS
E4–E12  = PASS
R4      = PASS
R5      = PASS
R6      = PASS
R7      = NEXT
NumPy   = AFTER R7
```

## Дорожная карта

Каноническая дорожная карта реализации: [REDMI.md](./REDMI.md)

Она определяет нормативный порядок qualification stages. Фактические статусы не выводятся из наличия раздела в дорожной карте, а подтверждаются CI/evidence и фиксируются в `Journal/EXPERIMENTS/EXPERIMENTS.md`.

## Синхронизация состояния

Нормативное правило перехода между этапами: [Journal/STATE_SYNCHRONIZATION.md](./Journal/STATE_SYNCHRONIZATION.md)

Операционная точка: [Journal/МАЯК.md](./Journal/МАЯК.md)

Фактическое подтверждённое состояние: [Journal/CURRENT_STATE.md](./Journal/CURRENT_STATE.md)

Следующий обязательный этап: [QUALIFICATION_NEXT.md](./QUALIFICATION_NEXT.md)

CI содержит отдельную проверку синхронизации состояния до запуска qualification tests.

## Нормативная база

Рабочие правила и фактическое состояние находятся в [Journal](./Journal/README.md). Источником истины являются committed source и воспроизводимое evidence.
